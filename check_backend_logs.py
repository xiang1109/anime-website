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
print("检查后端服务日志")
print("="*70)

# 1. 查看PM2日志
print("\n=== 1. 查看PM2日志（最后100行） ===")
out, err = run_command(ssh, "pm2 logs anime-backend --lines 100 --nostream")
print(out)
if err:
    print("错误:", err)

# 2. 查看PM2错误日志
print("\n=== 2. 查看PM2错误日志 ===")
out, err = run_command(ssh, "cat /root/.pm2/logs/anime-backend-error.log | tail -50")
print(out)

# 3. 查看PM2输出日志
print("\n=== 3. 查看PM2输出日志 ===")
out, err = run_command(ssh, "cat /root/.pm2/logs/anime-backend-out.log | tail -50")
print(out)

# 4. 检查后端服务状态
print("\n=== 4. 检查后端服务状态 ===")
out, err = run_command(ssh, "pm2 status anime-backend")
print(out)

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
