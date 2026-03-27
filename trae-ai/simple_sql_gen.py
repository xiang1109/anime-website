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

print("="*70)
print("最简单的SQL数据生成")
print("="*70)

# 1. 清空表
print("\n=== 1. 清空表 ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'TRUNCATE TABLE anime_db.animes;' 2>&1")

# 2. 生成SQL插入语句
print("\n=== 2. 生成SQL插入语句 ===")

# 直接在服务器上生成SQL
sql_gen_cmd = """
python3 -c "
import random
from datetime import datetime

anime_templates = [
    ('进击的巨人', '進撃の巨人', '在一个人类被巨人捕食的世界中', 'Wit Studio', '动作,奇幻,剧情'),
    ('海贼王', 'ONE PIECE', '蒙奇·D·路飞带领草帽海贼团', '东映动画', '冒险,动作,喜剧'),
    ('火影忍者', 'NARUTO -ナルト-', '关于忍者鸣人的成长故事', 'Studio Pierrot', '动作,冒险,剧情'),
    ('鬼灭之刃', '鬼滅の刃', '炭治郎拯救变成鬼的妹妹', 'ufotable', '动作,奇幻,历史'),
    ('咒术回战', '呪術廻戦', '虎杖悠仁进入咒术高专', 'MAPPA', '动作,奇幻,恐怖'),
]

values = []
for i in range(5000):
    template = random.choice(anime_templates)
    title = f'{template[0]} 第{i+1}季'
    title_jp = template[1]
    description = template[2]
    studio = template[3]
    genre = template[4]
    episodes = random.randint(12, 200)
    status = '完结' if random.random() > 0.5 else '连载中'
    release_year = random.randint(1990, 2025)
    cover_image = f'https://picsum.photos/300/400?random={i+1}'
    average_rating = round(random.uniform(7.0, 9.8), 2)
    rating_count = random.randint(1000, 50000)
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    values.append(f(\\\"{title}\\\", \\\"{title_jp}\\\", \\\"{description}\\\", \\\"{cover_image}\\\", {episodes}, \\\"{status}\\\", {release_year}, \\\"{studio}\\\", \\\"{genre}\\\", {average_rating}, {rating_count}, \\\"{created_at}\\\")

sql = 'USE anime_db; INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at) VALUES ' + ', '.join(values) + ';'
print(sql)
" > /tmp/insert_data.sql
"""

run_command(ssh, sql_gen_cmd)
print("SQL文件已生成")

# 3. 执行SQL
print("\n=== 3. 执行SQL（这可能需要几分钟） ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' < /tmp/insert_data.sql 2>&1", show=True)
print("SQL执行完成")

# 4. 检查数据量
print("\n=== 4. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 5. 检查数据示例
print("\n=== 5. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating FROM anime_db.animes LIMIT 3;' 2>&1")
print(out)

# 6. 测试API
print("\n=== 6. 测试API ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=5'")
print(out[:500])

# 7. 重启后端服务
print("\n=== 7. 重启后端服务 ===")
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
