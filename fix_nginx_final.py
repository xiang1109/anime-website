import paramiko
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("=== 1. 检查Nginx配置 ===")
out, err = run_command(ssh, "cat /etc/nginx/nginx.conf | grep -E 'include|server' | head -20")
print(out)

print("\n=== 2. 检查conf.d目录 ===")
out, err = run_command(ssh, "ls -la /etc/nginx/conf.d/")
print(out)

print("\n=== 3. 检查前端文件 ===")
out, err = run_command(ssh, "ls -la /opt/anime-website/frontend/")
print(out)

# 完全重写Nginx配置
print("\n=== 4. 重写Nginx配置 ===")
main_config = """
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name _;
        root /opt/anime-website/frontend;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass http://127.0.0.1:3001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
"""
run_command(ssh, f"cat > /etc/nginx/nginx.conf <<'EOF'\n{main_config}\nEOF")
run_command(ssh, "rm -f /etc/nginx/conf.d/*")

# 测试并重启
run_command(ssh, "nginx -t")
run_command(ssh, "systemctl restart nginx")
time.sleep(2)

print("\n=== 5. 测试访问 ===")
out, err = run_command(ssh, "curl -s -w '\\nHTTP Code: %{http_code}\\n' http://localhost/")
print("前端:", out[:200])

out, err = run_command(ssh, "curl -s http://localhost/api/health")
print("API:", out)

# 检查后端状态
print("\n=== 6. 后端状态 ===")
out, err = run_command(ssh, "pm2 status")
print(out)

ssh.close()

print("\n" + "="*60)
print("Nginx配置已完全重写！")
print("现在测试: ssh -L 8080:localhost:80 root@59.110.214.50")
print("然后访问: http://localhost:8080")
print("="*60)
