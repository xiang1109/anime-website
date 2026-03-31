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

def sftp_upload(ssh, local_path, remote_path):
    """上传文件或目录"""
    sftp = ssh.open_sftp()
    
    if os.path.isfile(local_path):
        print(f"上传文件: {local_path} -> {remote_path}")
        sftp.put(local_path, remote_path)
    elif os.path.isdir(local_path):
        try:
            sftp.mkdir(remote_path)
        except:
            pass
        for item in os.listdir(local_path):
            local_item = os.path.join(local_path, item)
            remote_item = f"{remote_path}/{item}"
            if os.path.isfile(local_item):
                print(f"上传文件: {local_item} -> {remote_item}")
                try:
                    sftp.put(local_item, remote_item)
                except Exception as e:
                    print(f"上传失败 {local_item}: {e}")
            elif os.path.isdir(local_item) and not item.startswith('.') and item != 'node_modules' and item != 'dist':
                sftp_upload(ssh, local_item, remote_item)
    sftp.close()

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"正在连接到 {hostname}...")
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("连接成功!")
        
        # 4. 部署后端代码
        print("\n=== 部署后端代码 ===")
        
        # 创建项目目录
        run_command(ssh, "mkdir -p /opt/anime-website/backend")
        
        # 打包本地代码（排除node_modules等）
        local_dir = "d:/code/trae-ai"
        
        # 上传必要的后端文件
        files_to_upload = [
            'server-simple.ts',
            'package.json',
            'package-lock.json',
            'tsconfig.json'
        ]
        
        sftp = ssh.open_sftp()
        for f in files_to_upload:
            local_path = f"{local_dir}/{f}"
            remote_path = f"/opt/anime-website/backend/{f}"
            print(f"上传: {f}")
            try:
                sftp.put(local_path, remote_path)
            except Exception as e:
                print(f"上传失败 {f}: {e}")
        sftp.close()
        
        # 安装后端依赖
        run_command(ssh, "cd /opt/anime-website/backend && npm install")
        
        # 安装tsx
        run_command(ssh, "cd /opt/anime-website/backend && npm install -g tsx typescript")
        
        # 修改后端配置中的数据库密码
        cmd = """
sed -i 's/123456/Xinmima1109/g' /opt/anime-website/backend/server-simple.ts
sed -i 's/localhost/59.110.214.50/g' /opt/anime-website/backend/server-simple.ts
        """
        run_command(ssh, cmd)
        
        # 5. 部署前端代码
        print("\n=== 部署前端代码 ===")
        
        # 本地构建前端
        print("本地构建前端...")
        os.chdir(local_dir)
        os.system("npm run build")
        
        # 上传构建产物
        run_command(ssh, "mkdir -p /opt/anime-website/frontend")
        
        # 使用sftp上传dist目录
        sftp = ssh.open_sftp()
        def upload_dir(local_dir, remote_dir):
            try:
                sftp.mkdir(remote_dir)
            except:
                pass
            for item in os.listdir(local_dir):
                local_path = os.path.join(local_dir, item)
                remote_path = f"{remote_dir}/{item}"
                if os.path.isfile(local_path):
                    print(f"上传: {local_path} -> {remote_path}")
                    sftp.put(local_path, remote_path)
                elif os.path.isdir(local_path):
                    upload_dir(local_path, remote_path)
        
        upload_dir(f"{local_dir}/dist", "/opt/anime-website/frontend")
        sftp.close()
        
        print("\n=== 代码部署完成! ===")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("连接已关闭")

if __name__ == '__main__':
    main()
