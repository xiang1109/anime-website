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
print("检查后端路由配置")
print("="*60)

# 1. 检查完整的后端代码
print("\n=== 1. 后端代码内容 ===")
out, err = run_command(ssh, "cat /opt/anime-website/backend/server-simple.ts")
print(out)

# 2. 测试所有可能的路由
print("\n=== 2. 测试所有路由 ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/health")
print("根路径/health:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/animes?page=1&limit=5")
print("/animes:", out[:300])

ssh.close()
