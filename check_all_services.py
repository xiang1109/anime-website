import paramiko
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show_output=True):
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if show_output:
        print(f"\n=== {command[:70]} ===")
        if out:
            print(out)
        if err:
            print("STDERR:", err)
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("=" * 60)
print("检查所有服务状态")
print("=" * 60)

# 1. 检查Nginx
run_command(ssh, "systemctl status nginx | head -20")

# 2. 检查后端服务
run_command(ssh, "pm2 status")
run_command(ssh, "pm2 logs anime-backend --lines 30")

# 3. 检查MySQL
run_command(ssh, "systemctl status mysqld | head -15")
run_command(ssh, "netstat -tlnp | grep -E '3001|80|3306'")

# 4. 测试本地访问
print("\n=== 测试本地访问 ===")
run_command(ssh, "curl -s -o /dev/null -w '%{http_code}' http://localhost/")
run_command(ssh, "curl -s http://localhost/api/health")

# 5. 检查防火墙
run_command(ssh, "systemctl status firewalld | head -10")
run_command(ssh, "firewall-cmd --list-ports 2>/dev/null || echo 'firewalld not running'")

# 6. 检查端口监听
run_command(ssh, "ss -tlnp | grep -E '80|3001|3306'")

ssh.close()
print("\n" + "=" * 60)
