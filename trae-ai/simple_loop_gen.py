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
print("生成5000条动漫数据")
print("="*70)

# 1. 清空表
print("\n=== 1. 清空表 ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'TRUNCATE TABLE anime_db.animes;' 2>&1")

# 2. 创建批量插入脚本
print("\n=== 2. 创建批量插入脚本 ===")

# 生成50个批量插入语句，每个插入100条数据
batch_script = ""
for batch in range(50):
    batch_script += "INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at) VALUES "
    values = []
    for i in range(100):
        idx = batch * 100 + i
        values.append(f"('动漫{idx+1}', 'アニメ{idx+1}', '这是关于冒险、友情和成长的故事', 'https://picsum.photos/300/400?random={idx+1}', 24, '连载中', 2020, 'Studio', '动作,冒险', 8.5, 1000, NOW())")
    batch_script += ", ".join(values) + ";\n"

# 写入脚本
sftp = ssh.open_sftp()
with sftp.file('/tmp/batch_insert.sql', 'w') as f:
    f.write("USE anime_db;\n" + batch_script)
sftp.close()
print("批量插入脚本已创建")

# 3. 执行批量插入
print("\n=== 3. 执行批量插入 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' < /tmp/batch_insert.sql 2>&1")
print("批量插入完成")

# 4. 检查数据量
print("\n=== 4. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 5. 检查数据示例
print("\n=== 5. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating FROM anime_db.animes ORDER BY id DESC LIMIT 5;' 2>&1")
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
