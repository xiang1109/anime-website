import random
from datetime import datetime

print("="*70)
print("生成本地SQL文件")
print("="*70)

# 动漫数据
anime_list = [
    "进击的巨人", "海贼王", "火影忍者", "鬼灭之刃", "咒术回战",
    "东京食尸鬼", "我的英雄学院", "刀剑神域", "名侦探柯南", "死亡笔记",
    "钢之炼金术师", "全职猎人", "命运石之门", "Code Geass", "CLANNAD",
    "银魂", "龙珠Z", "攻壳机动队", "黑礁", "虫师"
]

studio_list = [
    "Wit Studio", "东映动画", "Studio Pierrot", "ufotable", "MAPPA",
    "Madhouse", "Bones", "A-1 Pictures", "TMS Entertainment", "White Fox"
]

genre_list = [
    "动作,冒险,奇幻", "悬疑,犯罪,剧情", "爱情,剧情", "科幻,悬疑,剧情",
    "喜剧,动作", "动作,恐怖,剧情", "动作,冒险,喜剧"
]

# 生成SQL脚本
sql_script = "USE anime_db;\n\n"
sql_script += "TRUNCATE TABLE animes;\n\n"
sql_script += "INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at) VALUES\n"

values = []
for i in range(5000):
    title = random.choice(anime_list) + " 第" + str(i+1) + "季"
    title_jp = "アニメ" + str(i+1)
    description = "这是关于冒险、友情和成长的故事，讲述了主角们的精彩旅程。"
    cover_image = "https://picsum.photos/300/400?random=" + str(i+1)
    episodes = random.randint(12, 200)
    status = "完结" if random.random() > 0.5 else "连载中"
    release_year = random.randint(1990, 2025)
    studio = random.choice(studio_list)
    genre = random.choice(genre_list)
    average_rating = round(random.uniform(7.0, 9.8), 2)
    rating_count = random.randint(1000, 50000)
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    value = "('" + title + "', '" + title_jp + "', '" + description + "', '" + cover_image + "', " + str(episodes) + ", '" + status + "', " + str(release_year) + ", '" + studio + "', '" + genre + "', " + str(average_rating) + ", " + str(rating_count) + ", '" + created_at + "')"
    values.append(value)

sql_script += ",\n".join(values) + ";"

# 写入本地文件
with open('d:\\code\\trae-ai\\anime_data.sql', 'w', encoding='utf-8') as f:
    f.write(sql_script)

print("SQL文件已生成: d:\\code\\trae-ai\\anime_data.sql")
print("文件大小:", len(sql_script), "字节")

# 现在上传到服务器
print("\n" + "="*70)
print("上传到服务器")
print("="*70)

import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show=True):
    if show:
        print(f"\n执行: {command[:100]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if show and out:
        print(out)
    if show and err:
        print("ERR:", err)
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

# 上传文件
sftp = ssh.open_sftp()
sftp.put('d:\\code\\trae-ai\\anime_data.sql', '/tmp/anime_data.sql')
sftp.close()
print("文件已上传到服务器")

# 执行SQL
print("\n执行SQL（这可能需要几分钟）...")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' < /tmp/anime_data.sql 2>&1")
print("SQL执行完成")

# 检查数据量
print("\n检查数据量...")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 检查数据示例
print("\n检查数据示例...")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating FROM anime_db.animes ORDER BY id DESC LIMIT 5;' 2>&1")
print(out)

# 测试API
print("\n测试API...")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=5'")
print(out[:500])

# 重启后端服务
print("\n重启后端服务...")
run_command(ssh, "pm2 restart anime-backend 2>&1")
run_command(ssh, "sleep 2")

ssh.close()

print("\n" + "="*70)
print("数据生成完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在数据库中有5000条动漫数据！")
print("="*70)
