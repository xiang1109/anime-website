import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

# 检查后端路由
print("=== 检查后端路由 ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/health")
print("GET /health:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/health")
print("GET /api/health:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?limit=1 2>/dev/null | head -80")
print("GET /api/animes:", out)

# 查看server.ts中的路由定义
print("\n=== 查看后端路由定义 ===")
out, err = run_command(ssh, "cd /opt/anime-website/backend && grep -n 'app\\.' server-simple.ts | head -30")
print(out)

ssh.close()
