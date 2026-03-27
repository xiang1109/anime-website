import paramiko
import time

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

# 先停止服务
run_command(ssh, "pm2 delete anime-backend || true")
time.sleep(2)

# 直接运行查看错误
print("=== 直接运行后端查看错误 ===")
out, err = run_command(ssh, "cd /opt/anime-website/backend && timeout 10 tsx server-simple.ts 2>&1")
print(out)
print(err)

ssh.close()
