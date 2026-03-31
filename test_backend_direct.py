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
print("直接测试后端服务")
print("="*60)

# 1. 测试后端API
print("\n=== 1. 测试后端API ===")
out, err = run_command(ssh, "curl -v http://localhost:3001/api/health 2>&1")
print(out[:800])

out, err = run_command(ssh, "curl -v http://localhost:3001/api/animes 2>&1")
print(out[:800])

# 2. 检查后端日志
print("\n=== 2. 检查后端日志 ===")
out, err = run_command(ssh, "pm2 logs anime-backend --lines 20 --nostream 2>&1 | tail -30")
print(out)

# 3. 测试Nginx反向代理
print("\n=== 3. 测试Nginx反向代理 ===")
out, err = run_command(ssh, "curl -v http://localhost/api/health 2>&1")
print(out[:800])

out, err = run_command(ssh, "curl -v http://localhost/api/animes 2>&1")
print(out[:800])

ssh.close()

print("\n" + "="*60)
print("测试完成")
print("="*60)
