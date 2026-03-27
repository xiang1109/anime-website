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
print("检查后端代码路由定义")
print("="*60)

# 1. 搜索所有app.get定义
print("\n=== 1. 搜索所有GET路由 ===")
out, err = run_command(ssh, "grep -n 'app.get' /opt/anime-website/backend/server-simple.ts | head -30")
print(out)

# 2. 搜索animes相关的路由
print("\n=== 2. 搜索animes相关的路由 ===")
out, err = run_command(ssh, "grep -n 'animes' /opt/anime-website/backend/server-simple.ts | head -30")
print(out)

# 3. 测试不同的路由
print("\n=== 3. 测试不同的路由 ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("/api/health:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/health 2>&1")
print("/health:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes 2>&1")
print("/api/animes:", out[:200])

out, err = run_command(ssh, "curl -s http://localhost:3001/animes 2>&1")
print("/animes:", out[:200])

# 4. 检查代码中是否有/api前缀
print("\n=== 4. 检查/api前缀 ===")
out, err = run_command(ssh, "grep -n '/api' /opt/anime-website/backend/server-simple.ts | head -20")
print(out)

# 5. 检查app.use和app.listen
print("\n=== 5. 检查app.use和app.listen ===")
out, err = run_command(ssh, "grep -n -A2 -B2 'app.use' /opt/anime-website/backend/server-simple.ts | head -30")
print(out)

out, err = run_command(ssh, "grep -n -A5 'app.listen' /opt/anime-website/backend/server-simple.ts")
print(out)

# 6. 检查是否有其他问题
print("\n=== 6. 检查代码开头和结尾 ===")
out, err = run_command(ssh, "head -100 /opt/anime-website/backend/server-simple.ts")
print(out[:1000])

ssh.close()
