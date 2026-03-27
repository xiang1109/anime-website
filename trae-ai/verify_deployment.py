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
print("验证部署和数据更新")
print("="*70)

# 1. 验证后端服务
print("\n=== 1. 验证后端服务 ===")
out, err = run_command(ssh, "pm2 status anime-backend")
print(out)

# 2. 测试后端API
print("\n=== 2. 测试后端API ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/health'")
print(out)

# 3. 测试动漫列表API
print("\n=== 3. 测试动漫列表API ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime?page=1&limit=1'")
print(out[:500])

# 4. 测试动漫详情API
print("\n=== 4. 测试动漫详情API ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime/5011'")
print(out[:500])

# 5. 验证数据库中的动漫图片
print("\n=== 5. 验证数据库中的动漫图片 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, cover_image FROM anime_db.animes ORDER BY id LIMIT 5;' 2>&1")
print(out)

# 6. 验证前端文件
print("\n=== 6. 验证前端文件 ===")
out, err = run_command(ssh, "ls -la /usr/share/nginx/html/")
print(out)

# 7. 验证nginx配置
print("\n=== 7. 验证nginx配置 ===")
out, err = run_command(ssh, "nginx -t")
print(out)

# 8. 测试外部访问
print("\n=== 8. 测试外部访问 ===")
out, err = run_command(ssh, "curl -s 'http://localhost' -I | head -5")
print(out)

ssh.close()

print("\n" + "="*70)
print("验证完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在应该可以：")
print("1. 看到正确的React前端界面")
print("2. 看到真实的动漫图片（来自MyAnimeList）")
print("3. 点击动漫卡片查看详情")
print("4. 查看动漫的评论列表")
print("5. 登录后发表评论")
print("6. 登录后给动漫打分")
print("7. 使用搜索功能查找动漫")
print("="*70)
