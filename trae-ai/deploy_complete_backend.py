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
print("部署完整的后端代码")
print("="*70)

# 1. 备份当前后端文件
print("\n=== 1. 备份当前后端文件 ===")
run_command(ssh, "cp /opt/anime-website/backend/server-simple.ts /opt/anime-website/backend/server-simple.ts.bak")
print("备份完成")

# 2. 上传完整的后端文件
print("\n=== 2. 上传完整的后端文件 ===")
sftp = ssh.open_sftp()
sftp.put('d:/code/trae-ai/server-simple.ts', '/opt/anime-website/backend/server-simple.ts')
sftp.close()
print("文件上传完成")

# 3. 重启后端服务
print("\n=== 3. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend 2>&1")
run_command(ssh, "sleep 3")
print("服务重启完成")

# 4. 检查后端服务状态
print("\n=== 4. 检查后端服务状态 ===")
out, err = run_command(ssh, "pm2 status anime-backend")
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
print("部署完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在后端应该包含完整的评论和评分API！")
print("="*70)
