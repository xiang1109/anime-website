import paramiko
import subprocess

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
print("修复后端路由问题")
print("="*60)

# 1. 备份现有代码
print("\n=== 1. 备份现有代码 ===")
run_command(ssh, "cp /opt/anime-website/backend/server-simple.ts /opt/anime-website/backend/server-simple.ts.bak")

# 2. 读取本地代码并上传
print("\n=== 2. 上传本地代码 ===")
with open('d:/code/trae-ai/server-simple.ts', 'r', encoding='utf-8') as f:
    local_code = f.read()

# 创建临时文件
import tempfile
import os
with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
    f.write(local_code)
    temp_file = f.name

# 使用scp上传
try:
    result = subprocess.run(
        ['scp', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', 
         temp_file, f'root@{hostname}:/opt/anime-website/backend/server-simple.ts'],
        capture_output=True,
        text=True
    )
    print("上传结果:", result.returncode)
    if result.stderr:
        print("上传错误:", result.stderr)
finally:
    os.unlink(temp_file)

# 3. 重启后端服务
print("\n=== 3. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend")
run_command(ssh, "sleep 3")

# 4. 测试API
print("\n=== 4. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("/api/health:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=5 2>&1")
print("/api/animes:", out[:500])

# 5. 检查PM2状态
print("\n=== 5. 检查PM2状态 ===")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print(out)

ssh.close()

print("\n" + "="*60)
print("修复完成！")
print("请访问: http://59.110.214.50")
print("="*60)
