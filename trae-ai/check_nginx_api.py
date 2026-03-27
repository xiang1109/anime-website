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
print("检查Nginx API代理配置")
print("="*60)

# 1. 检查Nginx配置文件
print("\n=== 1. 检查Nginx配置文件 ===")
out, err = run_command(ssh, "cat /etc/nginx/nginx.conf")
print(out)

# 2. 测试Nginx API代理
print("\n=== 2. 测试Nginx API代理 ===")
out, err = run_command(ssh, "curl -v http://localhost/api/anime?page=1&limit=1 2>&1")
print(out[:500])

# 3. 测试直接访问后端
print("\n=== 3. 测试直接访问后端 ===")
out, err = run_command(ssh, "curl -v http://localhost:3001/api/anime?page=1&limit=1 2>&1")
print(out[:500])

ssh.close()

print("\n" + "="*60)
print("检查完成")
print("="*60)
