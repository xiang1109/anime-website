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

print("="*70)
print("检查后端文件内容")
print("="*70)

# 1. 查看后端文件的前200行
print("\n=== 1. 查看后端文件的前200行 ===")
out, err = run_command(ssh, "head -200 /opt/anime-website/backend/server-simple.ts")
print(out)

# 2. 查看后端文件的中间部分
print("\n=== 2. 查看后端文件的中间部分 ===")
out, err = run_command(ssh, "sed -n '400,600p' /opt/anime-website/backend/server-simple.ts")
print(out)

# 3. 查看后端文件的最后200行
print("\n=== 3. 查看后端文件的最后200行 ===")
out, err = run_command(ssh, "tail -200 /opt/anime-website/backend/server-simple.ts")
print(out)

# 4. 检查文件是否有语法错误
print("\n=== 4. 检查文件是否有语法错误 ===")
out, err = run_command(ssh, "cd /opt/anime-website/backend && npx tsc --noEmit server-simple.ts 2>&1 | head -50")
print(out)
if err:
    print("错误:", err)

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
