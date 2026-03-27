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
print("检查服务器上的后端目录")
print("="*70)

# 1. 查看/opt目录
print("\n=== 1. 查看/opt目录 ===")
out, err = run_command(ssh, "ls -la /opt/")
print(out)

# 2. 查看/opt/anime-website目录
print("\n=== 2. 查看/opt/anime-website目录 ===")
out, err = run_command(ssh, "ls -la /opt/anime-website/ 2>/dev/null || echo '目录不存在'")
print(out)

# 3. 查看/opt/anime-website/backend目录
print("\n=== 3. 查看/opt/anime-website/backend目录 ===")
out, err = run_command(ssh, "ls -la /opt/anime-website/backend/ 2>/dev/null || echo '目录不存在'")
print(out)

# 4. 查看/opt/anime-website/backend目录下的文件
print("\n=== 4. 查看/opt/anime-website/backend目录下的文件 ===")
out, err = run_command(ssh, "find /opt/anime-website/backend/ -type f -name '*.ts' -o -name '*.js' 2>/dev/null | head -20")
print(out)

# 5. 查看PM2配置
print("\n=== 5. 查看PM2配置 ===")
out, err = run_command(ssh, "pm2 show anime-backend | head -50")
print(out)

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
