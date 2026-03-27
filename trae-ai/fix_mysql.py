import paramiko
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    print(f"\n执行: {command[:80]}...")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=120)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if out:
        print(out)
    if err:
        print(f"STDERR: {err}")
    return stdout.channel.recv_exit_status()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("=== 检查MySQL状态 ===")
run_command(ssh, "systemctl status mysqld | head -10")

print("\n=== 直接修改后端配置为使用空密码测试 ===")
run_command(ssh, """
cd /opt/anime-website/backend && \
cat server-simple.ts | grep -A10 createConnection
""")

print("\n=== 测试各种MySQL密码 ===")
run_command(ssh, "mysql -u root -e 'SELECT 1' 2>&1 | head -5")
run_command(ssh, "mysql -u root -p'' -e 'SELECT 1' 2>&1 | head -5")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT 1' 2>&1 | head -5")

ssh.close()
