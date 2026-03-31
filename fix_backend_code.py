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
print("检查并修复后端代码")
print("="*60)

# 1. 检查PM2配置
print("\n=== 1. 检查PM2配置 ===")
out, err = run_command(ssh, "pm2 show anime-backend 2>&1 | grep -E 'script|cwd|pid|status' | head -10")
print(out)

# 2. 检查后端目录
print("\n=== 2. 检查后端目录 ===")
out, err = run_command(ssh, "ls -la /opt/anime-website/backend/")
print(out)

# 3. 直接运行后端代码
print("\n=== 3. 直接运行后端代码 ===")
run_command(ssh, "cd /opt/anime-website/backend && ls -la")

# 4. 检查是否有其他后端文件
print("\n=== 4. 检查后端文件 ===")
out, err = run_command(ssh, "find /opt/anime-website/ -name '*.ts' -o -name '*.js' | head -20")
print(out)

# 5. 检查server-simple.ts的路径
print("\n=== 5. 检查server-simple.ts ===")
out, err = run_command(ssh, "ls -lh /opt/anime-website/backend/server-simple.ts")
print(out)

# 6. 停止PM2，直接测试直接运行测试
print("\n=== 6. 直接运行测试 ===")
run_command(ssh, "pm2 delete anime-backend 2>&1")
run_command(ssh, "sleep 2")

# 7. 用node直接运行
print("\n=== 7. 用node直接运行 ===")
run_command(ssh, "cd /opt/anime-website/backend && npm run server:prod 2>&1 &")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "ps aux | grep -E 'tsx|node' | grep -v grep | head -5")
print(out)

# 8. 测试API
print("\n=== 8. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print(out)

ssh.close()
