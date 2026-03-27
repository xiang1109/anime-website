import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show=True):
    if show:
        print(f"\n执行: {command[:100]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if show and out:
        print(out)
    if show and err:
        print("ERR:", err)
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("="*60)
print("修复Nginx配置")
print("="*60)

# 1. 创建正确的Nginx配置
print("\n=== 1. 创建正确的Nginx配置 ===")
nginx_config = """user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        include /etc/nginx/default.d/*.conf;

        location /api/ {
            proxy_pass http://localhost:3001;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        location / {
            try_files $uri $uri/ /index.html;
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
}
"""
run_command(ssh, f"cat > /etc/nginx/nginx.conf <<'EOF'\n{nginx_config}\nEOF")
print("Nginx配置已更新")

# 2. 测试Nginx配置
print("\n=== 2. 测试Nginx配置 ===")
out, err = run_command(ssh, "nginx -t")
print(out)

# 3. 重启Nginx
print("\n=== 3. 重启Nginx ===")
run_command(ssh, "systemctl restart nginx")
run_command(ssh, "sleep 2")

# 4. 测试Nginx API代理
print("\n=== 4. 测试Nginx API代理 ===")
out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1")
print("Nginx API:", out[:100])

# 5. 测试直接访问后端
print("\n=== 5. 测试直接访问后端 ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/anime?page=1&limit=1")
print("后端API:", out[:100])

ssh.close()

print("\n" + "="*60)
print("Nginx配置修复完成！")
print("="*60)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在应该能看到动漫数据了！")
print("="*60)
