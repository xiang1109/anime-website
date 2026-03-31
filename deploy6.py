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
        
        # 修复Nginx配置和后端服务
        print("\n=== 修复配置和服务 ===")
        
        # 1. 先停止所有服务
        run_command(ssh, "pkill -f node || true")
        run_command(ssh, "systemctl stop nginx")
        
        # 2. 清理PM2并重新安装
        run_command(ssh, "npm uninstall -g pm2 && npm install -g pm2")
        
        # 3. 修改Nginx配置 - 简化版本
        nginx_config = """
server {
    listen 80;
    server_name _;
    
    # 前端静态文件
    location / {
        root /opt/anime-website/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API
    location /api/ {
        proxy_pass http://localhost:3001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
        # 写入配置
        cmd = f"cat > /etc/nginx/conf.d/anime-website.conf <<'EOF'\n{nginx_config}\nEOF"
        run_command(ssh, cmd)
        
        # 4. 删除默认配置并测试
        run_command(ssh, "rm -f /etc/nginx/conf.d/default.conf")
        run_command(ssh, "nginx -t")
        
        # 5. 启动Nginx
        run_command(ssh, "systemctl start nginx")
        
        # 6. 修改后端配置文件 - 使用正确的MySQL主机
        run_command(ssh, """
sed -i 's/host: ".*"/host: "127.0.0.1"/' /opt/anime-website/backend/server-simple.ts
sed -i 's/password: ".*"/password: "Xinmima1109"/' /opt/anime-website/backend/server-simple.ts
        """)
        
        # 7. 使用PM2启动后端
        run_command(ssh, """
cd /opt/anime-website/backend && \
pm2 delete anime-backend || true && \
pm2 start "tsx server-simple.ts" --name anime-backend && \
sleep 5 && \
pm2 status
        """)
        
        # 8. 验证服务
        print("\n=== 验证服务状态 ===")
        run_command(ssh, "pm2 status")
        run_command(ssh, "systemctl status nginx | head -20")
        
        # 9. 测试API
        print("\n=== 测试API ===")
        run_command(ssh, "sleep 3 && curl -v http://localhost:3001/api/health")
        run_command(ssh, "curl -v http://localhost/api/health")
        
        print("\n=== 配置完成! ===")
        print(f"网站地址: http://{hostname}")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("连接已关闭")

if __name__ == '__main__':
    main()
