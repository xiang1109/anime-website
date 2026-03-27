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
print("检查服务器上的后端代码")
print("="*70)

# 1. 查看后端目录
print("\n=== 1. 查看后端目录 ===")
out, err = run_command(ssh, "ls -la /root/anime-backend/")
print(out)

# 2. 查看后端文件
print("\n=== 2. 查看后端文件 ===")
out, err = run_command(ssh, "cat /root/anime-backend/server-simple.ts | head -100")
print(out)

# 3. 查看PM2状态
print("\n=== 3. 查看PM2状态 ===")
out, err = run_command(ssh, "pm2 status")
print(out)

# 4. 查看后端日志
print("\n=== 4. 查看后端日志 ===")
out, err = run_command(ssh, "pm2 logs anime-backend --lines 50 --nostream")
print(out)

# 5. 测试后端API
print("\n=== 5. 测试后端API ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/health'")
print(out)

# 6. 测试动漫详情API
print("\n=== 6. 测试动漫详情API ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime/1'")
print(out[:500])

# 7. 测试评论API
print("\n=== 7. 测试评论API ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime/1/comments'")
print(out[:500])

# 8. 测试评分API
print("\n=== 8. 测试评分API ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime/1/user-rating' -H 'Authorization: Bearer invalid'")
print(out[:500])

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
