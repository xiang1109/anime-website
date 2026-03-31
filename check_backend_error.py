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
print("检查后端服务错误日志")
print("="*60)

# 1. 检查PM2日志
print("\n=== 1. 检查PM2日志 ===")
out, err = run_command(ssh, "pm2 logs anime-backend --lines 50 --nostream 2>&1 | tail -100")
print(out)

# 2. 检查后端进程
print("\n=== 2. 检查后端进程 ===")
out, err = run_command(ssh, "ps aux | grep -E 'tsx|node' | grep -v grep | head -5")
print(out)

# 3. 检查端口监听
print("\n=== 3. 检查端口监听 ===")
out, err = run_command(ssh, "ss -tlnp | grep 3001")
print(out)

# 4. 直接测试后端代码
print("\n=== 4. 直接测试后端代码 ===")
run_command(ssh, "pkill -9 -f 'tsx|node' 2>&1 || true")
run_command(ssh, "sleep 2")
out, err = run_command(ssh, "cd /opt/anime-website/backend && npx tsx server-simple.ts 2>&1 &")
run_command(ssh, "sleep 5")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("/api/health:", out)
out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=5 2>&1")
print("/api/animes:", out[:500])

# 5. 用PM2重新启动
print("\n=== 5. 用PM2重新启动 ===")
run_command(ssh, "pkill -9 -f 'tsx|node' 2>&1 || true")
run_command(ssh, "sleep 2")
run_command(ssh, "cd /opt/anime-website/backend && pm2 start server-simple.ts --interpreter tsx --name anime-backend 2>&1")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print(out)

# 6. 再次测试
print("\n=== 6. 再次测试API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("/api/health:", out)
out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=5 2>&1")
print("/api/animes:", out[:500])

ssh.close()
