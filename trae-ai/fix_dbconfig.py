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

# 读取dbConfig配置
out, err = run_command(ssh, "cd /opt/anime-website/backend && grep -B2 -A10 'dbConfig' server-simple.ts")
print("当前dbConfig配置:")
print(out)

# 用sed替换密码
run_command(ssh, "cd /opt/anime-website/backend && sed -i \"s/password: '[^']*'/password: 'Xinmima1109'/\" server-simple.ts")
run_command(ssh, "cd /opt/anime-website/backend && sed -i 's/password: \"[^\"]*\"/password: \"Xinmima1109\"/' server-simple.ts")

# 再次检查
out, err = run_command(ssh, "cd /opt/anime-website/backend && grep -B2 -A10 'dbConfig' server-simple.ts")
print("\n修改后的dbConfig配置:")
print(out)

# 重启服务
run_command(ssh, "pm2 delete anime-backend || true")
run_command(ssh, "cd /opt/anime-website/backend && pm2 start 'tsx server-simple.ts' --name anime-backend")

# 等待并检查日志
import time
time.sleep(5)
out, err = run_command(ssh, "pm2 logs anime-backend --lines 30")
print("\n服务日志:")
print(out[-1000:])

ssh.close()
