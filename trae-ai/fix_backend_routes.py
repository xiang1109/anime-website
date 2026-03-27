import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show=True):
    if show:
        print(f"\n执行: {command[:80]}...")
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
print("检查并修复后端路由")
print("="*60)

# 1. 检查完整的后端代码
print("\n=== 1. 检查后端代码 ===")
out, err = run_command(ssh, "wc -l /opt/anime-website/backend/server-simple.ts")
print(f"代码行数: {out.strip()}")

# 2. 搜索是否有/api/animes路由
print("\n=== 2. 搜索/api/animes路由 ===")
out, err = run_command(ssh, "grep -n 'api/animes' /opt/anime-website/backend/server-simple.ts")
print(out)

# 3. 读取本地的server-simple.ts
print("\n=== 3. 读取本地后端代码 ===")
with open('d:/code/trae-ai/server-simple.ts', 'r', encoding='utf-8') as f:
    local_code = f.read()

# 4. 上传本地代码到服务器
print("\n=== 4. 上传本地代码到服务器 ===")
run_command(ssh, "cp /opt/anime-website/backend/server-simple.ts /opt/anime-website/backend/server-simple.ts.bak")

# 5. 写入本地代码到服务器
from tempfile import NamedTemporaryFile
import os

with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
    f.write(local_code)
    temp_file = f.name

# 上传文件
import subprocess
subprocess.run(['scp', '-o', 'StrictHostKeyChecking=no', temp_file, f'root@{hostname}:/opt/anime-website/backend/server-simple.ts'], capture_output=True)
os.unlink(temp_file)

# 6. 重启后端服务
print("\n=== 5. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend")
run_command(ssh, "sleep 3")

# 7. 测试API
print("\n=== 6. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("/api/health:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=5 2>&1")
print("/api/animes:", out[:500])

ssh.close()

print("\n" + "="*60)
print("修复完成！")
print("="*60)
