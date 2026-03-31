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
print("检查所有API端点")
print("="*60)

# 1. 检查前端所有API调用
print("\n=== 1. 前端所有API调用 ===")
out, err = run_command(ssh, "grep -r 'fetch.*api' /opt/anime-website/src/ --include='*.tsx' | sort")
print(out)

# 2. 测试所有可能的API端点
print("\n=== 2. 测试API端点 ===")
endpoints = [
    '/api/health',
    '/api/anime',
    '/api/animes',
    '/api/anime/1',
    '/api/animes/1',
    '/api/auth/login',
    '/api/auth/register',
    '/api/admin/animes',
]

for endpoint in endpoints:
    out, err = run_command(ssh, f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:3001{endpoint} 2>&1", show=False)
    status = out.strip()
    print(f"{endpoint}: {status}")

# 3. 检查后端所有路由
print("\n=== 3. 后端所有路由 ===")
out, err = run_command(ssh, "grep -n 'app\\.' /opt/anime-website/backend/server-simple.ts | grep -E 'get|post|put|delete'")
print(out)

ssh.close()

print("\n" + "="*60)
print("检查完成")
print("="*60)
