import paramiko
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    print(f"\n执行: {command[:60]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if out:
        print(out)
    if err:
        print("STDERR:", err[:500])
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("=== 启动后端服务 ===")
run_command(ssh, "pm2 delete anime-backend || true")
run_command(ssh, "cd /opt/anime-website/backend && pm2 start 'tsx server-simple.ts' --name anime-backend")

time.sleep(5)

print("\n=== 检查服务状态 ===")
run_command(ssh, "pm2 status")
run_command(ssh, "pm2 logs anime-backend --lines 20")

print("\n=== 测试API ===")
run_command(ssh, "curl http://localhost:3001/api/health")
run_command(ssh, "curl http://localhost:3001/api/animes?page=1&limit=5 2>/dev/null | head -100")

ssh.close()
