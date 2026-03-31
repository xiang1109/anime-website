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

print("=== 检查后端服务状态 ===")
out, err = run_command(ssh, "pm2 status")
print(out)

print("\n=== 检查后端服务日志 ===")
out, err = run_command(ssh, "pm2 logs anime-backend --lines 20")
print(out[-1500:])

print("\n=== 测试后端API ===")
out, err = run_command(ssh, "curl -v http://localhost:3001/api/health 2>&1")
print(out)

ssh.close()
