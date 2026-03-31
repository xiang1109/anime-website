import paramiko
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, timeout=30):
    print(f"\n执行: {command[:80]}...")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    start = time.time()
    while not stdout.channel.exit_status_ready() and time.time() - start < timeout:
        time.sleep(0.5)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if out:
        print(out[:500])
    if err:
        print(f"STDERR: {err[:500]}")
    return stdout.channel.recv_exit_status()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("=== 重置MySQL密码 ===")

# 创建重置脚本
reset_script = """
#!/bin/bash
systemctl stop mysqld
pkill -9 mysqld
sleep 2

# 启动跳过授权模式
mysqld --user=mysql --skip-grant-tables --skip-networking &
sleep 5

# 修改密码
mysql -u root <<EOF
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Xinmima1109';
EOF

# 重启
pkill -9 mysqld
sleep 3
systemctl start mysqld
sleep 5
"""
run_command(ssh, f"cat > /tmp/reset_mysql.sh <<'EOF'\n{reset_script}\nEOF")
run_command(ssh, "chmod +x /tmp/reset_mysql.sh && /tmp/reset_mysql.sh", timeout=60)

print("\n=== 测试密码 ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT USER(), NOW()'", timeout=10)

print("\n=== 修改后端代码密码 ===")
run_command(ssh, """
cd /opt/anime-website/backend && \
sed -i 's/password: "[^"]*"/password: "Xinmima1109"/' server-simple.ts && \
cat server-simple.ts | grep -A5 password
""")

# 重启服务
print("\n=== 重启后端服务 ===")
run_command(ssh, "pm2 delete anime-backend || true")
run_command(ssh, "cd /opt/anime-website/backend && pm2 start 'tsx server-simple.ts' --name anime-backend")
time.sleep(5)
run_command(ssh, "pm2 logs anime-backend --lines 20")

ssh.close()
