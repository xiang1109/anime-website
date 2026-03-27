import paramiko
import os
from datetime import datetime

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

def run_local_command(command, show=True):
    if show:
        print(f"\n本地执行: {command[:100]}...")
    result = os.popen(command).read()
    if show and result:
        print(result)
    return result

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("="*70)
print("完整部署流程（包含Git提交）")
print("="*70)

# 1. 本地Git提交
print("\n=== 1. 本地Git提交 ===")
run_local_command("git add .")
commit_message = f"Deploy update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
run_local_command(f"git commit -m \"{commit_message}\"")
run_local_command("git push origin main")

# 2. 服务器上拉取最新代码
print("\n=== 2. 服务器上拉取最新代码 ===")
run_command(ssh, "cd /var/www/anime-website && git pull origin main")

# 3. 安装依赖
print("\n=== 3. 安装依赖 ===")
run_command(ssh, "cd /var/www/anime-website && npm install")

# 4. 构建前端
print("\n=== 4. 构建前端 ===")
run_command(ssh, "cd /var/www/anime-website && npm run build")

# 5. 重启后端服务
print("\n=== 5. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend")

# 6. 重启Nginx
print("\n=== 6. 重启Nginx ===")
run_command(ssh, "systemctl restart nginx")

# 7. 验证部署
print("\n=== 7. 验证部署 ===")
run_command(ssh, "pm2 status anime-backend")
run_command(ssh, "systemctl status nginx --no-pager | head -5")

# 8. 测试API
print("\n=== 8. 测试API ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=5'")
print(out[:500])

ssh.close()

print("\n" + "="*70)
print("部署完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n数据库中有5000+条动漫数据！")
print("="*70)
