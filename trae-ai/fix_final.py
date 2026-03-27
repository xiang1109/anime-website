import paramiko
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("=== 1. 修复Nginx代理配置 ===")
# Nginx配置中的proxy_pass有问题，需要去掉末尾的斜杠
nginx_config = """
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /opt/anime-website/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
cmd = f"cat > /etc/nginx/conf.d/anime-website.conf <<'EOF'\n{nginx_config}\nEOF"
run_command(ssh, cmd)
run_command(ssh, "systemctl restart nginx")
time.sleep(2)

# 测试Nginx代理
out, err = run_command(ssh, "curl -s http://localhost/api/health")
print("Nginx代理测试:", out[:50])

print("\n=== 2. 导入动漫数据 ===")
# 从本地获取anime数据SQL
import os
anime_sql = ""
if os.path.exists("d:/code/trae-ai/anime_data.sql"):
    with open("d:/code/trae-ai/anime_data.sql", "r", encoding="utf-8") as f:
        anime_sql = f.read()
else:
    # 创建一些示例数据
    anime_sql = """
USE anime_db;
INSERT IGNORE INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count) VALUES
('进击的巨人', '進撃の巨人', '在一个人类被巨人捕食的世界中，主角艾伦·耶格尔加入调查兵团与巨人战斗', 'https://picsum.photos/300/400?random=1', 87, '完结', 2013, 'Wit Studio', '动作,奇幻,剧情', 9.5, 15000),
('海贼王', 'ONE PIECE', '蒙奇·D·路飞带领草帽海贼团寻找传说中的One Piece', 'https://picsum.photos/300/400?random=2', 1100, '连载中', 1999, '东映动画', '冒险,动作,喜剧', 9.2, 20000),
('火影忍者', 'NARUTO -ナルト-', '关于忍者鸣人的成长故事', 'https://picsum.photos/300/400?random=3', 720, '完结', 2002, 'Studio Pierrot', '动作,冒险,剧情', 8.9, 18000),
('鬼灭之刃', '鬼滅の刃', '炭治郎为了拯救变成鬼的妹妹而踏上旅程', 'https://picsum.photos/300/400?random=4', 55, '连载中', 2019, 'ufotable', '动作,奇幻,历史', 9.4, 12000),
('咒术回战', '呪術廻戦', '虎杖悠仁进入咒术高专学习咒术', 'https://picsum.photos/300/400?random=5', 47, '连载中', 2020, 'MAPPA', '动作,奇幻,恐怖', 9.1, 10000),
('东京食尸鬼', '東京喰種トーキョーグール', '金木研变成食尸鬼后的故事', 'https://picsum.photos/300/400?random=6', 48, '完结', 2014, 'Studio Pierrot', '动作,恐怖,剧情', 8.5, 9000),
('我的英雄学院', '僕のヒーローアカデミア', '在大部分人都有超能力的世界中，无能力的绿谷出久也想成为英雄', 'https://picsum.photos/300/400?random=7', 138, '连载中', 2016, 'Bones', '动作,冒险,喜剧', 8.3, 8500),
('刀剑神域', 'ソードアート・オンライン', 'VR游戏中的生存冒险', 'https://picsum.photos/300/400?random=8', 96, '连载中', 2012, 'A-1 Pictures', '动作,冒险,奇幻', 8.1, 11000),
('名侦探柯南', '名探偵コナン', '工藤新一变成小学生柯南后破案的故事', 'https://picsum.photos/300/400?random=9', 1100, '连载中', 1996, 'TMS Entertainment', '悬疑,犯罪,动画', 8.7, 25000),
('死亡笔记', 'DEATH NOTE', '天才少年夜神月捡到可以杀人的笔记本', 'https://picsum.photos/300/400?random=10', 37, '完结', 2006, 'Madhouse', '悬疑,犯罪,剧情', 9.3, 16000);
"""

# 上传并执行SQL
cmd = f"cat > /tmp/insert_anime.sql <<'EOF'\n{anime_sql}\nEOF"
run_command(ssh, cmd)
run_command(ssh, "mysql -u root -p'Xinmima1109' < /tmp/insert_anime.sql 2>&1 | head -10")

# 验证数据
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes'")
print("动漫数据条数:", out)

print("\n=== 3. 最终测试 ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=3' 2>/dev/null | head -150")
print("动漫列表API:", out)

ssh.close()

print("\n=== 部署完成！===")
print(f"🌐 网站访问地址: http://{hostname}")
print(f"👑 管理员账号: admin / admin123")
