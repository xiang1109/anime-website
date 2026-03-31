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

print("="*60)
print("检查API路由匹配")
print("="*60)

# 1. 检查后端路由
print("\n=== 1. 后端路由 ===")
out, err = run_command(ssh, "grep -n 'app\\.' /opt/anime-website/backend/server-simple.ts | head -30")
print(out)

# 2. 检查前端API调用
print("\n=== 2. 前端API调用 ===")
out, err = run_command(ssh, "grep -r 'fetch.*api' /opt/anime-website/src/ --include='*.tsx' | head -20")
print(out)

# 3. 测试所有可能的API路径
print("\n=== 3. 测试API路径 ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/anime?page=1&limit=1 2>&1")
print("/api/anime:", out[:100])

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=1 2>&1")
print("/api/animes:", out[:100])

# 4. 检查Nginx配置
print("\n=== 4. Nginx配置 ===")
out, err = run_command(ssh, "cat /etc/nginx/nginx.conf | grep -A20 'location /api'")
print(out)

# 5. 测试通过Nginx的API调用
print("\n=== 5. 通过Nginx测试API ===")
out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1 2>&1")
print("/api/anime (Nginx):", out[:100])

out, err = run_command(ssh, "curl -s http://localhost/api/animes?page=1&limit=1 2>&1")
print("/api/animes (Nginx):", out[:100])

ssh.close()

print("\n" + "="*60)
print("检查完成")
print("="*60)
