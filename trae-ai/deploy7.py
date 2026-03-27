import paramiko
import time
import os

# 服务器配置
hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, timeout=600):
    print(f"\n=== 执行命令: {command[:100]}... ===")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    output = []
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            line = stdout.channel.recv(1024).decode('utf-8', errors='ignore')
            print(line, end='')
            output.append(line)
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

def sftp_upload_file(sftp, local_path, remote_path):
    """上传单个文件"""
    try:
        sftp.put(local_path, remote_path)
        print(f"上传成功: {local_path} -> {remote_path}")
        return True
    except Exception as e:
        print(f"上传失败: {local_path} -> {remote_path}: {e}")
        return False

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"正在连接到 {hostname}...")
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("连接成功!")
        
        # 1. 准备目录
        run_command(ssh, "mkdir -p /opt/anime-website/backend")
        run_command(ssh, "mkdir -p /opt/anime-website/frontend")
        
        # 2. 上传后端文件
        print("\n=== 上传后端文件 ===")
        local_dir = "d:/code/trae-ai"
        sftp = ssh.open_sftp()
        
        backend_files = ['server-simple.ts', 'package.json', 'package-lock.json', 'tsconfig.json']
        for f in backend_files:
            local_path = f"{local_dir}/{f}"
            remote_path = f"/opt/anime-website/backend/{f}"
            sftp_upload_file(sftp, local_path, remote_path)
        
        # 3. 修改后端配置
        print("\n=== 修改后端配置 ===")
        run_command(ssh, """
cd /opt/anime-website/backend && \
sed -i 's/host: "localhost"/host: "127.0.0.1"/' server-simple.ts && \
sed -i 's/password: "123456"/password: "Xinmima1109"/' server-simple.ts
        """)
        
        # 4. 安装依赖
        print("\n=== 安装后端依赖 ===")
        run_command(ssh, "cd /opt/anime-website/backend && npm install")
        run_command(ssh, "npm install -g tsx typescript")
        
        # 5. 启动后端服务
        print("\n=== 启动后端服务 ===")
        run_command(ssh, """
cd /opt/anime-website/backend && \
pm2 delete anime-backend || true && \
pm2 start "tsx server-simple.ts" --name anime-backend
        """)
        
        time.sleep(5)
        run_command(ssh, "pm2 status && pm2 logs anime-backend --lines 20")
        
        # 6. 测试后端API
        print("\n=== 测试后端API ===")
        run_command(ssh, "curl http://localhost:3001/api/health")
        
        sftp.close()
        print("\n=== 后端部署完成! ===")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("连接已关闭")

if __name__ == '__main__':
    main()
