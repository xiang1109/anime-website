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
print("检查真实动漫数据")
print("="*70)

# 1. 检查数据量
print("\n=== 1. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 2. 检查前10条数据的图片URL
print("\n=== 2. 检查前10条数据 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, cover_image FROM anime_db.animes LIMIT 10;' 2>&1")
print(out)

# 3. 检查图片URL类型
print("\n=== 3. 检查图片URL类型 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT cover_image FROM anime_db.animes LIMIT 1;' 2>&1")
print(out)

# 4. 检查数据示例
print("\n=== 4. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, description, average_rating FROM anime_db.animes LIMIT 3;' 2>&1")
print(out)

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
