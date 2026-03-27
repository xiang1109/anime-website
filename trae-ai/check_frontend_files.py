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
print("检查服务器上的前端文件")
print("="*70)

# 检查前端目录
print("\n=== 1. 检查前端目录 ===")
out, err = run_command(ssh, "ls -la /usr/share/nginx/html/")
print(out)

# 检查index.html
print("\n=== 2. 检查index.html ===")
out, err = run_command(ssh, "cat /usr/share/nginx/html/index.html | head -50")
print(out)

# 检查assets目录
print("\n=== 3. 检查assets目录 ===")
out, err = run_command(ssh, "ls -la /usr/share/nginx/html/assets/")
print(out)

# 检查是否有备份
print("\n=== 4. 检查是否有备份 ===")
out, err = run_command(ssh, "ls -la /root/")
print(out)

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
