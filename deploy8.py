import paramiko
import time

# 服务器配置
hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, timeout=600):
    print(f"\n=== 执行命令: {command[:100]}... ===")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            line = stdout.channel.recv(1024).decode('utf-8', errors='ignore')
            print(line, end='')
        if stderr.channel.recv_stderr_ready():
            line = stderr.channel.recv_stderr(1024).decode('utf-8', errors='ignore')
            print(f"STDERR: {line}", end='')
        time.sleep(0.1)
    exit_status = stdout.channel.recv_exit_status()
    remaining = stdout.read().decode('utf-8', errors='ignore')
    if remaining:
        print(remaining, end='')
    print(f"\n命令执行完成，退出码: {exit_status}")
    return exit_status

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"正在连接到 {hostname}...")
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("连接成功!")
        
        # 1. 重置MySQL root密码并授权
        print("\n=== 重置MySQL密码 ===")
        run_command(ssh, """
# 重置MySQL密码
systemctl stop mysqld
pkill -9 mysqld
sleep 2

# 跳过授权启动
mysqld --user=mysql --skip-grant-tables --skip-networking &
sleep 5

# 修改密码
mysql -u root -e "
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Xinmima1109';
"

# 重启MySQL
pkill -9 mysqld
sleep 2
systemctl start mysqld
sleep 5
        """)
        
        # 2. 创建anime_user用户并授权
        print("\n=== 创建数据库用户 ===")
        run_command(ssh, """
mysql -u root -p'Xinmima1109' -e "
CREATE USER IF NOT EXISTS 'anime_user'@'%' IDENTIFIED BY 'Xinmima1109';
GRANT ALL PRIVILEGES ON anime_db.* TO 'anime_user'@'%';
FLUSH PRIVILEGES;
SELECT user, host FROM mysql.user WHERE user LIKE '%anime%';
"
        """)
        
        # 3. 修改后端配置使用anime_user
        print("\n=== 修改后端配置 ===")
        run_command(ssh, """
cd /opt/anime-website/backend && \
sed -i 's/user: "root"/user: "anime_user"/' server-simple.ts && \
sed -i 's/password: ".*"/password: "Xinmima1109"/' server-simple.ts && \
sed -i 's/database: ".*"/database: "anime_db"/' server-simple.ts
        """)
        
        # 4. 显示当前配置
        run_command(ssh, "grep -A5 'createConnection' /opt/anime-website/backend/server-simple.ts")
        
        # 5. 重启后端服务
        print("\n=== 重启后端服务 ===")
        run_command(ssh, """
pm2 delete anime-backend || true && \
cd /opt/anime-website/backend && \
pm2 start "tsx server-simple.ts" --name anime-backend && \
sleep 5 && \
pm2 logs anime-backend --lines 30
        """)
        
        # 6. 测试API
        print("\n=== 测试API ===")
        run_command(ssh, "curl http://localhost:3001/api/health")
        
        print("\n=== 配置完成! ===")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("连接已关闭")

if __name__ == '__main__':
    main()
