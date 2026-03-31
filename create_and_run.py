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
print("创建并运行Python脚本")
print("="*70)

# 1. 创建Python脚本文件
print("\n=== 1. 创建Python脚本文件 ===")

# 先创建一个简单的脚本，不使用f-string
python_script = '''
import mysql.connector
import random
from datetime import datetime

conn = mysql.connector.connect(
    host='localhost',
    database='anime_db',
    user='root',
    password='Xinmima1109'
)
cursor = conn.cursor()

anime_list = ['进击的巨人', '海贼王', '火影忍者', '鬼灭之刃', '咒术回战']
studio_list = ['Wit Studio', '东映动画', 'Studio Pierrot', 'ufotable', 'MAPPA']
genre_list = ['动作,冒险,奇幻', '悬疑,犯罪,剧情', '爱情,剧情', '科幻,悬疑']

insert_query = 'INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

total = 5000
batch_size = 100

print('开始生成', total, '条数据...')

for batch in range(0, total, batch_size):
    values = []
    for i in range(batch_size):
        idx = batch + i
        title = random.choice(anime_list) + ' 第' + str(idx+1) + '季'
        title_jp = 'アニメ' + str(idx+1)
        description = '这是关于冒险、友情和成长的故事'
        cover_image = 'https://picsum.photos/300/400?random=' + str(idx+1)
        episodes = random.randint(12, 200)
        status = '完结' if random.random() > 0.5 else '连载中'
        release_year = random.randint(1990, 2025)
        studio = random.choice(studio_list)
        genre = random.choice(genre_list)
        average_rating = round(random.uniform(7.0, 9.8), 2)
        rating_count = random.randint(1000, 50000)
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        values.append((title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at))
    
    cursor.executemany(insert_query, values)
    conn.commit()
    print('已插入', batch + batch_size, '条记录')

print('完成！')
cursor.execute('SELECT COUNT(*) FROM animes')
print('总记录数:', cursor.fetchone()[0])

cursor.close()
conn.close()
'''

# 使用echo命令创建文件（更简单的方法）
run_command(ssh, "echo '" + python_script + "' > /tmp/simple_gen.py")
print("Python脚本文件已创建")

# 检查文件是否存在
out, err = run_command(ssh, "ls -la /tmp/simple_gen.py")
print(out)

# 2. 安装依赖
print("\n=== 2. 安装依赖 ===")
run_command(ssh, "pip3 install mysql-connector-python 2>&1 | tail -3")

# 3. 运行脚本
print("\n=== 3. 运行脚本 ===")
out, err = run_command(ssh, "python3 /tmp/simple_gen.py 2>&1")
print(out)
print(err)

# 4. 检查数据量
print("\n=== 4. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 5. 检查数据示例
print("\n=== 5. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating FROM anime_db.animes ORDER BY id DESC LIMIT 5;' 2>&1")
print(out)

ssh.close()

print("\n" + "="*70)
print("脚本执行完成")
print("="*70)
