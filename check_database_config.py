import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show=True):
    if show:
        print(f"\n执行: {command[:80]}...")
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

print("="*60)
print("检查数据库配置和服务状态")
print("="*60)

# 1. 检查MySQL服务状态
print("\n=== 1. MySQL服务状态 ===")
out, err = run_command(ssh, "systemctl status mysqld | grep -E 'Active|PID'")
print(out)

# 2. 检查数据库配置
print("\n=== 2. 后端数据库配置 ===")
out, err = run_command(ssh, "cat /opt/anime-website/backend/.env 2>/dev/null || cat /opt/anime-website/backend/.env")
print(out)

# 3. 检查数据库连接
print("\n=== 3. 测试数据库连接 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SHOW DATABASES;' 2>&1")
print(out)

# 4. 检查动漫数据
print("\n=== 4. 检查动漫数据 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' anime_db -e 'SELECT COUNT(*) FROM animes;' 2>&1")
print(out)

# 5. 检查后端服务状态
print("\n=== 5. 后端服务状态 ===")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print(out)

# 6. 测试后端API
print("\n=== 6. 测试后端API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health")
print("健康检查:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=5 2>&1")
print("动漫列表:", out[:500])

ssh.close()

print("\n" + "="*60)
print("数据库信息：")
print("="*60)
print("主机: localhost")
print("数据库: anime_db")
print("用户名: root")
print("密码: Xinmima1109")
print("="*60)
