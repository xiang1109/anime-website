import paramiko
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    print(f"\n执行: {command[:80]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if out:
        print(out[:300])
    if err:
        print("STDERR:", err[:200])
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

# 检查Nginx配置文件
print("=== 检查Nginx配置 ===")
run_command(ssh, "ls -la /etc/nginx/conf.d/")
run_command(ssh, "cat /etc/nginx/nginx.conf | grep -A30 'http {' | grep -E 'include|default_type'")

# 清理所有配置，只保留我们的
run_command(ssh, "rm -f /etc/nginx/conf.d/*.conf")

# 创建新的配置
nginx_config = """
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /opt/anime-website/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:3001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
cmd = f"cat > /etc/nginx/conf.d/anime-website.conf <<'EOF'\n{nginx_config}\nEOF"
run_command(ssh, cmd)

# 修改主配置文件，移除默认server
run_command(ssh, "sed -i '/server.*default_server/,+20d' /etc/nginx/nginx.conf 2>/dev/null || true")

# 测试并重启Nginx
run_command(ssh, "nginx -t")
run_command(ssh, "systemctl stop nginx && sleep 2 && systemctl start nginx")
time.sleep(3)

# 测试访问
print("\n=== 测试访问 ===")
run_command(ssh, "curl -s -I http://localhost/")
run_command(ssh, "curl -s http://localhost/api/health")

ssh.close()

print(f"\n=== 完成！===")
print(f"网站: http://{hostname}")
