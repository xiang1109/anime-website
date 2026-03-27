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
print("修复后端API问题")
print("="*60)

# 1. 检查后端代码
print("\n=== 1. 检查后端代码 ===")
out, err = run_command(ssh, "ls -la /opt/anime-website/backend/")
print(out)

# 2. 检查主文件
print("\n=== 2. 检查主文件 ===")
out, err = run_command(ssh, "cat /opt/anime-website/backend/server-simple.ts | head -50")
print(out[:500])

# 3. 检查数据库配置
print("\n=== 3. 创建.env文件 ===")
env_content = """DB_HOST=localhost
DB_USER=root
DB_PASSWORD=Xinmima1109
DB_NAME=anime_db
DB_PORT=3306
PORT=3001
JWT_SECRET=your-secret-key-change-this-in-production
"""
run_command(ssh, f"cat > /opt/anime-website/backend/.env <<'EOF'\n{env_content}\nEOF")

# 4. 重启后端服务
print("\n=== 4. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print(out)

# 5. 测试API
print("\n=== 5. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health")
print("健康检查:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=5 2>&1")
print("动漫列表:", out[:500])

# 6. 检查后端日志
print("\n=== 6. 检查后端日志 ===")
out, err = run_command(ssh, "pm2 logs anime-backend --lines 20 --nostream 2>&1 | tail -30")
print(out[:800])

ssh.close()

print("\n" + "="*60)
print("修复完成！")
print("="*60)
