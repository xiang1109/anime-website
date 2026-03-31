import paramiko
import random
from datetime import datetime

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
print("最简单的5000条数据生成")
print("="*70)

# 1. 清空表
print("\n=== 1. 清空表 ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'TRUNCATE TABLE anime_db.animes;' 2>&1")

# 2. 创建Python脚本
print("\n=== 2. 创建Python脚本 ===")

python_script = """#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='anime_db',
        user='root',
        password='Xinmima1109'
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # 动漫数据模板
        anime_data = [
            ("进击的巨人", "進撃の巨人", "在一个人类被巨人捕食的世界中，主角艾伦·耶格尔加入调查兵团与巨人战斗", "Wit Studio", "动作,奇幻,剧情", 87, "完结", 2013),
            ("海贼王", "ONE PIECE", "蒙奇·D·路飞带领草帽海贼团寻找传说中的One Piece", "东映动画", "冒险,动作,喜剧", 1100, "连载中", 1999),
            ("火影忍者", "NARUTO -ナルト-", "关于忍者鸣人的成长故事", "Studio Pierrot", "动作,冒险,剧情", 720, "完结", 2002),
            ("鬼灭之刃", "鬼滅の刃", "炭治郎为了拯救变成鬼的妹妹而踏上旅程", "ufotable", "动作,奇幻,历史", 55, "连载中", 2019),
            ("咒术回战", "呪術廻戦", "虎杖悠仁进入咒术高专学习咒术", "MAPPA", "动作,奇幻,恐怖", 47, "连载中", 2020),
            ("东京食尸鬼", "東京喰種トーキョーグール", "金木研变成食尸鬼后的故事", "Studio Pierrot", "动作,恐怖,剧情", 48, "完结", 2014),
            ("我的英雄学院", "僕のヒーローアカデミア", "在大部分人都有超能力的世界中，无能力的绿谷出久也想成为英雄", "Bones", "动作,冒险,喜剧", 138, "连载中", 2016),
            ("刀剑神域", "ソードアート・オンライン", "VR游戏中的生存冒险", "A-1 Pictures", "动作,冒险,奇幻", 96, "连载中", 2012),
            ("名侦探柯南", "名探偵コナン", "工藤新一变成小学生柯南后破案的故事", "TMS Entertainment", "悬疑,犯罪,动画", 1100, "连载中", 1996),
            ("死亡笔记", "DEATH NOTE", "天才少年夜神月捡到可以杀人的笔记本", "Madhouse", "悬疑,犯罪,剧情", 37, "完结", 2006),
            ("钢之炼金术师", "鋼の錬金術師", "爱德华和阿尔冯斯寻找贤者之石的旅程", "Bones", "动作,冒险,奇幻", 64, "完结", 2009),
            ("全职猎人", "HUNTER×HUNTER", "小杰为了寻找父亲而成为猎人的故事", "Madhouse", "动作,冒险,奇幻", 148, "完结", 2011),
        ]
        
        insert_query = "INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        total = 5000
        batch_size = 100
        
        for batch in range(0, total, batch_size):
            values = []
            for i in range(batch_size):
                idx = batch + i
                template = random.choice(anime_data)
                title = f"{template[0]} 第{idx+1}季"
                title_jp = template[1]
                description = template[2]
                studio = template[3]
                genre = template[4]
                episodes = template[5] + random.randint(-10, 50)
                status = template[6]
                release_year = template[7] + random.randint(-5, 5)
                cover_image = f"https://picsum.photos/300/400?random={idx+1}"
                average_rating = round(random.uniform(7.0, 9.8), 2)
                rating_count = random.randint(1000, 50000)
                created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                values.append((title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at))
            
            cursor.executemany(insert_query, values)
            connection.commit()
            print(f"已插入 {batch + batch_size} 条记录")
        
        print(f"\\n总共插入 {total} 条记录")
        
except Error as e:
    print(f"数据库错误: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
"""

run_command(ssh, f"cat > /tmp/simple_data_gen.py <<'EOF'\n{python_script}\nEOF")
print("Python脚本已创建")

# 3. 安装依赖
print("\n=== 3. 安装依赖 ===")
run_command(ssh, "pip3 install mysql-connector-python 2>&1 | tail -3")

# 4. 运行脚本
print("\n=== 4. 运行数据生成脚本 ===")
out, err = run_command(ssh, "python3 /tmp/simple_data_gen.py 2>&1", show=True)
print("脚本执行完成")

# 5. 检查数据量
print("\n=== 5. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 6. 检查数据示例
print("\n=== 6. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating, cover_image FROM anime_db.animes LIMIT 3;' 2>&1")
print(out)

# 7. 测试API
print("\n=== 7. 测试API ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=3'")
print(out[:500])

# 8. 重启后端服务
print("\n=== 8. 重启后端服务 ===")
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
