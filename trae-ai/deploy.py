import paramiko
import time

# 服务器配置
hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, timeout=600):
    """执行SSH命令并打印输出"""
    print(f"\n=== 执行命令: {command[:100]}... ===")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    
    # 实时输出
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            line = stdout.channel.recv(1024).decode('utf-8')
            print(line, end='')
        if stderr.channel.recv_stderr_ready():
            line = stderr.channel.recv_stderr(1024).decode('utf-8')
            print(f"STDERR: {line}", end='')
        time.sleep(0.1)
    
    # 读取剩余输出
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
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"正在连接到 {hostname}...")
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("连接成功!")
        
        # 1. 系统更新和软件安装
        commands = [
            # 安装 MySQL 8.0 (使用正确的包名)
            'yum install -y mysql-server',
            # 安装 Nginx
            'yum install -y nginx',
            # 验证安装
            'node -v && npm -v && mysqld --version && nginx -v',
            # 启动并启用MySQL
            'systemctl start mysqld && systemctl enable mysqld',
            # 启动并启用Nginx
            'systemctl start nginx && systemctl enable nginx',
            # 检查服务状态
            'systemctl status mysqld | head -20 && systemctl status nginx | head -20',
        ]
        
        for cmd in commands:
            if run_command(ssh, cmd) != 0:
                print(f"命令执行失败: {cmd}")
                # 继续执行下一个命令而不是返回
                continue
        
        print("\n=== 基础软件安装完成! ===")
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        ssh.close()
        print("连接已关闭")

if __name__ == '__main__':
    main()
