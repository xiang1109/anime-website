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
print("检查数据库表")
print("="*70)

# 1. 查看所有表
print("\n=== 1. 查看所有表 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SHOW TABLES FROM anime_db;' 2>&1")
print(out)

# 2. 查看comments表结构
print("\n=== 2. 查看comments表结构 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'DESCRIBE anime_db.comments;' 2>&1")
print(out)

# 3. 查看ratings表结构
print("\n=== 3. 查看ratings表结构 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'DESCRIBE anime_db.ratings;' 2>&1")
print(out)

# 4. 查看comments表数据量
print("\n=== 4. 查看comments表数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.comments;' 2>&1")
print(out)

# 5. 查看ratings表数据量
print("\n=== 5. 查看ratings表数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.ratings;' 2>&1")
print(out)

# 6. 查看comments表示例数据
print("\n=== 6. 查看comments表示例数据 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT * FROM anime_db.comments LIMIT 3;' 2>&1")
print(out)

# 7. 查看ratings表示例数据
print("\n=== 7. 查看ratings表示例数据 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT * FROM anime_db.ratings LIMIT 3;' 2>&1")
print(out)

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
