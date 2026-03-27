import paramiko
import time
import os

# 服务器配置
hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, timeout=600):
    """执行SSH命令并打印输出"""
    print(f"\n=== 执行命令: {command[:100]}... ===")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            line = stdout.channel.recv(1024).decode('utf-8')
            print(line, end='')
        if stderr.channel.recv_stderr_ready():
            line = stderr.channel.recv_stderr(1024).decode('utf-8')
            print(f"STDERR: {line}", end='')
        time.sleep(0.1)
    
    exit_status = stdout.channel.recv_exit_status()
    remaining = stdout.read().decode('utf-8')
    if remaining:
        print(remaining, end='')
    remaining_err = stderr.read().decode('utf-8')
    if remaining_err:
        print(f"STDERR: {remaining_err}", end='')
    
    print(f"\n命令执行完成，退出码: {exit_status}")
    return exit_status

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"正在连接到 {hostname}...")
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("连接成功!")
        
        # 2. 配置MySQL数据库
        print("\n=== 配置MySQL数据库 ===")
        
        # 获取MySQL临时密码
        cmd = "grep 'temporary password' /var/log/mysqld.log | head -1 | awk '{print $NF}'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        temp_password = stdout.read().decode('utf-8').strip()
        print(f"MySQL临时密码: {temp_password}")
        
        # 设置新密码和创建数据库
        mysql_commands = f"""
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Xinmima1109';
CREATE DATABASE IF NOT EXISTS anime_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'anime_user'@'%' IDENTIFIED BY 'Xinmima1109';
GRANT ALL PRIVILEGES ON anime_db.* TO 'anime_user'@'%';
FLUSH PRIVILEGES;
SHOW DATABASES;
"""
        # 将命令写入临时文件
        cmd = f"echo \"{mysql_commands}\" > /tmp/mysql_init.sql"
        run_command(ssh, cmd)
        
        # 执行MySQL命令
        cmd = f"mysql -u root -p'{temp_password}' --connect-expired-password < /tmp/mysql_init.sql"
        run_command(ssh, cmd)
        
        # 验证数据库连接
        cmd = "mysql -u anime_user -p'Xinmima1109' -e 'SELECT DATABASE();'"
        run_command(ssh, cmd)
        
        # 3. 创建数据库表
        print("\n=== 创建数据库表 ===")
        sql_script = """
USE anime_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    avatar VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS animes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    title_jp VARCHAR(255),
    description TEXT,
    cover_image VARCHAR(500),
    episodes INT DEFAULT 0,
    status VARCHAR(50),
    release_year INT,
    studio VARCHAR(100),
    genre VARCHAR(255),
    average_rating DECIMAL(3,2) DEFAULT 0.00,
    rating_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    anime_id INT,
    rating DECIMAL(2,1) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_anime (user_id, anime_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (anime_id) REFERENCES animes(id)
);

CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    anime_id INT,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (anime_id) REFERENCES animes(id)
);

CREATE TABLE IF NOT EXISTS verification_codes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    used BOOLEAN DEFAULT FALSE
);

-- 创建admin用户
INSERT IGNORE INTO users (username, email, password) VALUES 
('admin', 'admin@example.com', '$2a$10$CwTycUXWue0Thq9StjUM0uJ8EvrMc96y3FyG.1r8zG6xkyV9Q6O');

SHOW TABLES;
"""
        # 写入SQL文件
        cmd = f"cat > /tmp/create_tables.sql <<'EOF'\n{sql_script}\nEOF"
        run_command(ssh, cmd)
        
        # 执行SQL
        cmd = "mysql -u anime_user -p'Xinmima1109' < /tmp/create_tables.sql"
        run_command(ssh, cmd)
        
        print("\n=== 数据库配置完成! ===")
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        ssh.close()
        print("连接已关闭")

if __name__ == '__main__':
    main()
