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
print("检查服务器部署情况")
print("="*70)

# 1. 检查文件系统
print("\n=== 1. 检查文件系统 ===")
run_command(ssh, "ls -la /var/www/")
run_command(ssh, "ls -la /opt/")

# 2. 检查Nginx配置
print("\n=== 2. 检查Nginx配置 ===")
run_command(ssh, "cat /etc/nginx/nginx.conf | head -50")
run_command(ssh, "ls -la /etc/nginx/conf.d/")

# 3. 检查后端服务
print("\n=== 3. 检查后端服务 ===")
run_command(ssh, "pm2 list")
run_command(ssh, "pm2 show anime-backend | head -20")

# 4. 测试后端API（直接访问端口）
print("\n=== 4. 测试后端API（直接访问端口） ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime?page=1&limit=5' 2>&1")
print(out[:500])

# 5. 测试Nginx代理
print("\n=== 5. 测试Nginx代理 ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=5' 2>&1")
print(out[:500])

# 6. 检查数据库
print("\n=== 6. 检查数据库 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
