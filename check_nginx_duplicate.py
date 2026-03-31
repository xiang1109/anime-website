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

print("="*70)
print("检查Nginx重复的server块")
print("="*70)

# 1. 检查所有Nginx配置文件
print("\n=== 1. 检查所有Nginx配置文件 ===")
out, err = run_command(ssh, "ls -la /etc/nginx/")
print(out)

out, err = run_command(ssh, "ls -la /etc/nginx/conf.d/")
print(out)

# 2. 检查是否有默认配置文件
print("\n=== 2. 检查默认配置文件 ===")
out, err = run_command(ssh, "cat /etc/nginx/conf.d/default.conf 2>&1")
print(out[:500])

# 3. 查看完整的Nginx配置
print("\n=== 3. 查看完整的Nginx配置 ===")
out, err = run_command(ssh, "nginx -T 2>&1 | head -100")
print(out[:1000])

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
