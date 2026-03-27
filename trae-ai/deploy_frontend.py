import paramiko
import os
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'
local_dir = "d:/code/trae-ai"

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

def upload_dir(sftp, local_path, remote_path):
    """递归上传目录"""
    if not os.path.exists(local_path):
        print(f"本地目录不存在: {local_path}")
        return
    
    try:
        sftp.mkdir(remote_path)
    except:
        pass
    
    for item in os.listdir(local_path):
        local_item = os.path.join(local_path, item)
        remote_item = f"{remote_path}/{item}"
        
        if os.path.isfile(local_item):
            print(f"上传: {local_item} -> {remote_item}")
            try:
                sftp.put(local_item, remote_item)
            except Exception as e:
                print(f"上传失败: {e}")
        elif os.path.isdir(local_item):
            upload_dir(sftp, local_item, remote_item)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

# 1. 本地构建前端
print("=== 本地构建前端 ===")
os.chdir(local_dir)
result = os.system("npm run build")
if result != 0:
    print("构建失败，尝试安装依赖...")
    os.system("npm install")
    os.system("npm run build")

# 2. 上传前端文件
print("\n=== 上传前端文件 ===")
sftp = ssh.open_sftp()
upload_dir(sftp, f"{local_dir}/dist", "/opt/anime-website/frontend")
sftp.close()

# 3. 检查上传结果
run_command(ssh, "ls -la /opt/anime-website/frontend/")
run_command(ssh, "ls -la /opt/anime-website/frontend/assets/ | head -10")

# 4. 修复Nginx配置
print("\n=== 修复Nginx配置 ===")
nginx_config = """
server {
    listen 80;
    server_name _;
    
    root /opt/anime-website/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
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

# 移除默认配置
run_command(ssh, "rm -f /etc/nginx/conf.d/default.conf")

# 测试并重启Nginx
run_command(ssh, "nginx -t && systemctl restart nginx")

# 5. 测试访问
print("\n=== 测试网站访问 ===")
time.sleep(2)
run_command(ssh, "curl -s http://localhost/ | head -5")
run_command(ssh, "curl -s http://localhost/api/health")

ssh.close()

print(f"\n=== 前端部署完成！===")
print(f"网站访问地址: http://{hostname}")
