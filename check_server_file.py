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
print("检查服务器上的后端文件内容")
print("="*70)

# 1. 查看后端文件的评论和评分路由
print("\n=== 1. 查看后端文件的评论和评分路由 ===")
out, err = run_command(ssh, "grep -n 'comments\\|rate\\|rating' /opt/anime-website/backend/server-simple.ts | head -50")
print(out)

# 2. 查看后端文件的所有路由
print("\n=== 2. 查看后端文件的所有路由 ===")
out, err = run_command(ssh, "grep -n 'app\\.(get\\|post\\|put\\|delete)' /opt/anime-website/backend/server-simple.ts | head -100")
print(out)

# 3. 查看后端文件的总行数
print("\n=== 3. 查看后端文件的总行数 ===")
out, err = run_command(ssh, "wc -l /opt/anime-website/backend/server-simple.ts")
print(out)

# 4. 查看后端文件的最后100行
print("\n=== 4. 查看后端文件的最后100行 ===")
out, err = run_command(ssh, "tail -100 /opt/anime-website/backend/server-simple.ts")
print(out)

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
