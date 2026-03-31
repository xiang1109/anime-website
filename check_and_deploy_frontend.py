import paramiko
import os
import tarfile
import tempfile

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
print("检查并重新部署前端")
print("="*60)

# 1. 检查服务器上的前端文件
print("\n=== 1. 检查服务器上的前端文件 ===")
out, err = run_command(ssh, "ls -la /opt/anime-website/")
print(out)

# 2. 检查本地文件
print("\n=== 2. 检查本地文件 ===")
local_files = os.listdir('.')
print("本地文件:", local_files)

# 3. 打包本地前端文件
print("\n=== 3. 打包本地前端文件 ===")
with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp:
    tmp_name = tmp.name

with tarfile.open(tmp_name, 'w:gz') as tar:
    for item in ['src', 'package.json', 'tsconfig.json', 'tsconfig.node.json', 'vite.config.ts', 'index.html']:
        if os.path.exists(item):
            tar.add(item)
            print(f"添加: {item}")

# 4. 上传到服务器
print("\n=== 4. 上传到服务器 ===")
sftp = ssh.open_sftp()
sftp.put(tmp_name, '/tmp/frontend.tar.gz')
sftp.close()
print("上传完成")

# 5. 解压文件
print("\n=== 5. 解压文件 ===")
run_command(ssh, "cd /opt/anime-website && tar -xzf /tmp/frontend.tar.gz")
run_command(ssh, "rm /tmp/frontend.tar.gz")

# 6. 安装依赖并构建
print("\n=== 6. 安装依赖并构建 ===")
run_command(ssh, "cd /opt/anime-website && npm install 2>&1 | tail -10")
run_command(ssh, "cd /opt/anime-website && npm run build 2>&1 | tail -20")

# 7. 复制构建产物到Nginx
print("\n=== 7. 复制构建产物到Nginx ===")
run_command(ssh, "rm -rf /usr/share/nginx/html/*")
run_command(ssh, "cp -r /opt/anime-website/dist/* /usr/share/nginx/html/")
run_command(ssh, "chown -R nginx:nginx /usr/share/nginx/html/")

# 8. 重启Nginx
print("\n=== 8. 重启Nginx ===")
run_command(ssh, "systemctl restart nginx")

# 9. 测试
print("\n=== 9. 测试 ===")
out, err = run_command(ssh, "curl -s http://localhost/api/health")
print("健康检查:", out)
out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1")
print("动漫数据:", out[:200])

# 清理临时文件
os.unlink(tmp_name)

ssh.close()

print("\n" + "="*60)
print("前端部署完成！")
print("="*60)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("="*60)
