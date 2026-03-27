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
print("服务器端数据生成")
print("="*70)

# 创建Python脚本
print("\n=== 1. 创建Python脚本 ===")

# 使用简单的字符串拼接
python_script = '''#!/usr/bin/env python3
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
        
        # 清空表
        cursor.execute("TRUNCATE TABLE animes")
        connection.commit()
        print("已清空表")
        
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
        
        insert_query = "INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        total = 5000
        batch_size = 100
        
        print("开始生成", total, "条数据...")
        
        for batch in range(0, total, batch_size):
            values = []
            for i in range(batch_size):
                idx = batch + i
                title = random.choice(anime_list) + " 第" + str(idx+1) + "季"
                title_jp = "アニメ" + str(idx+1)
                description = "这是关于冒险、友情和成长的故事，讲述了主角们的精彩旅程。"
                cover_image = "https://picsum.photos/300/400?random=" + str(idx+1)
                episodes = random.randint(12, 200)
                status = "完结" if random.random() > 0.5 else "连载中"
                release_year = random.randint(1990, 2025)
                studio = random.choice(studio_list)
                genre = random.choice(genre_list)
                average_rating = round(random.uniform(7.0, 9.8), 2)
                rating_count = random.randint(1000, 50000)
                created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                values.append((title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at))
            
            cursor.executemany(insert_query, values)
            connection.commit()
            print("已插入", batch + batch_size, "条记录")
        
        print("\\n总共插入", total, "条记录")
        
        # 验证数据
        cursor.execute("SELECT COUNT(*) FROM animes")
        count = cursor.fetchone()[0]
        print("数据库中实际记录数:", count)
        
except Error as e:
    print("数据库错误:", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
'''

# 写入脚本
sftp = ssh.open_sftp()
with sftp.file('/tmp/server_gen.py', 'w') as f:
    f.write(python_script)
sftp.close()
print("Python脚本已写入")

# 安装依赖
print("\n=== 2. 安装依赖 ===")
run_command(ssh, "pip3 install mysql-connector-python 2>&1 | tail -3")

# 运行脚本
print("\n=== 3. 运行数据生成脚本 ===")
out, err = run_command(ssh, "python3 /tmp/server_gen.py 2>&1", show=True)
print("脚本执行完成")

# 检查数据量
print("\n=== 4. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 检查数据示例
print("\n=== 5. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating FROM anime_db.animes ORDER BY id DESC LIMIT 5;' 2>&1")
print(out)

# 测试API
print("\n=== 6. 测试API ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=5'")
print(out[:500])

# 重启后端服务
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
