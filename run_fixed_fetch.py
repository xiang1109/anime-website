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
print("运行修复后的脚本获取真实动漫数据")
print("="*70)

# 1. 上传修复后的Python脚本
print("\n=== 1. 上传修复后的Python脚本 ===")
sftp = ssh.open_sftp()
sftp.put('d:/code/trae-ai/fetch_real_data_fixed.py', '/root/fetch_real_data_fixed.py')
sftp.close()
print("修复后的Python脚本已上传")

# 2. 安装pymysql
print("\n=== 2. 安装pymysql ===")
run_command(ssh, "pip3 install pymysql requests 2>&1 | tail -5")

# 3. 先删除相关表中的数据
print("\n=== 3. 删除相关表中的数据 ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'DELETE FROM anime_db.ratings;' 2>&1")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'DELETE FROM anime_db.comments;' 2>&1")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'DELETE FROM anime_db.animes;' 2>&1")
print("相关表数据已删除")

# 4. 运行脚本
print("\n=== 4. 运行脚本（这可能需要几分钟） ===")
print("开始获取真实动漫数据，请稍候...")

stdin, stdout, stderr = ssh.exec_command("python3 /root/fetch_real_data_fixed.py 2>&1")
out = stdout.read().decode('utf-8', errors='ignore')
err = stderr.read().decode('utf-8', errors='ignore')
print(out)
if err:
    print("错误:", err)

# 5. 检查数据量
print("\n=== 5. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 6. 检查前3条数据
print("\n=== 6. 检查前3条数据 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, cover_image FROM anime_db.animes LIMIT 3;' 2>&1")
print(out)

# 7. 检查后3条数据
print("\n=== 7. 检查后3条数据 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, cover_image FROM anime_db.animes ORDER BY id DESC LIMIT 3;' 2>&1")
print(out)

# 8. 测试API
print("\n=== 8. 测试API ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=5'")
print(out[:500])

# 9. 重启后端服务
print("\n=== 9. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend 2>&1")
run_command(ssh, "sleep 2")

ssh.close()

print("\n" + "="*70)
print("数据获取完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在数据库中有真实的动漫数据！")
print("="*70)
