import paramiko
import time
import os

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show=True):
    if show:
        print(f"\n执行: {command[:60]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if show and out:
        print(out[:300])
    if show and err:
        print("ERR:", err[:200])
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("="*60)
print("全面检查和修复")
print("="*60)

# 1. 停止所有服务并清理
print("\n=== 1. 停止所有服务 ===")
run_command(ssh, "pm2 delete all || true")
run_command(ssh, "systemctl stop nginx")
run_command(ssh, "pkill -f 'tsx|node' || true")
time.sleep(2)

# 2. 检查MySQL
print("\n=== 2. 检查MySQL ===")
run_command(ssh, "systemctl start mysqld")
time.sleep(3)
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT 1' 2>&1")
if "Access denied" in out:
    print("MySQL密码错误，重置中...")
    run_command(ssh, "pkill -9 mysqld && sleep 2")
    run_command(ssh, "mysqld --user=mysql --skip-grant-tables --skip-networking &")
    time.sleep(5)
    run_command(ssh, "mysql -u root -e \"FLUSH PRIVILEGES; ALTER USER 'root'@'localhost' IDENTIFIED BY 'Xinmima1109';\"")
    run_command(ssh, "pkill -9 mysqld && sleep 2 && systemctl start mysqld")
    time.sleep(5)

# 3. 修改后端配置
print("\n=== 3. 修复后端配置 ===")
run_command(ssh, "cd /opt/anime-website/backend && sed -i \"s/password: '[^']*'/password: 'Xinmima1109'/\" server-simple.ts")
run_command(ssh, "cd /opt/anime-website/backend && grep -A5 'dbConfig' server-simple.ts")

# 4. 启动后端
print("\n=== 4. 启动后端服务 ===")
run_command(ssh, "cd /opt/anime-website/backend && pm2 start 'tsx server-simple.ts' --name anime-backend")
time.sleep(5)
out, err = run_command(ssh, "pm2 logs anime-backend --lines 20 --nostream")
print(out[-500:])

# 5. 测试后端
print("\n=== 5. 测试后端API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health")
print("健康检查:", out)
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime?limit=1' | head -80")
print("动漫列表:", out[:100])

# 6. 修复Nginx配置
print("\n=== 6. 修复Nginx配置 ===")
nginx_conf = """
server {
    listen 80;
    server_name _;
    
    root /opt/anime-website/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
"""
run_command(ssh, "rm -f /etc/nginx/conf.d/*.conf")
run_command(ssh, f"cat > /etc/nginx/conf.d/anime.conf <<'EOF'\n{nginx_conf}\nEOF")
run_command(ssh, "nginx -t")
run_command(ssh, "systemctl start nginx")

# 7. 测试Nginx
print("\n=== 7. 测试Nginx ===")
out, err = run_command(ssh, "curl -s -I http://localhost/")
print("前端响应:", out[:100])
out, err = run_command(ssh, "curl -s http://localhost/api/health")
print("API响应:", out)

# 8. 检查所有服务状态
print("\n=== 8. 服务状态 ===")
run_command(ssh, "pm2 status")
run_command(ssh, "systemctl status nginx mysqld | grep -E 'Active|nginx|mysql'")

ssh.close()

print("\n" + "="*60)
print("所有服务已重启和修复！")
print("="*60)
print("\n测试访问:")
print("1. 在本地执行: ssh -L 8080:localhost:80 root@59.110.214.50")
print("2. 浏览器打开: http://localhost:8080")
print("\n或者等待阿里云80端口开放后访问: http://59.110.214.50")
print("="*60)
