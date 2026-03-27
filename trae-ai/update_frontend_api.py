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

print("="*60)
print("更新前端API地址")
print("="*60)

# 1. 查看当前前端API配置
print("\n=== 1. 查看当前前端API配置 ===")
out, err = run_command(ssh, "grep -r 'localhost:3001' /opt/anime-website/src/ --include='*.tsx' --include='*.ts' | head -10")
print(out)

# 2. 替换所有localhost:3001为空字符串（使用相对路径）
print("\n=== 2. 替换API地址为相对路径 ===")
run_command(ssh, "sed -i 's|http://localhost:3001||g' /opt/anime-website/src/pages/*.tsx")
run_command(ssh, "sed -i 's|http://localhost:3001||g' /opt/anime-website/src/components/*.tsx")
run_command(ssh, "sed -i 's|http://localhost:3001||g' /opt/anime-website/src/context/*.tsx")
print("已替换所有API地址为相对路径")

# 3. 验证替换结果
print("\n=== 3. 验证替换结果 ===")
out, err = run_command(ssh, "grep -r 'localhost:3001' /opt/anime-website/src/ --include='*.tsx' --include='*.ts' | head -10")
if out:
    print("还有未替换的地址:", out)
else:
    print("所有localhost:3001地址已替换")

# 4. 重新构建前端
print("\n=== 4. 重新构建前端 ===")
run_command(ssh, "cd /opt/anime-website && npm run build 2>&1 | tail -20")

# 5. 复制构建产物到Nginx
print("\n=== 5. 复制构建产物到Nginx ===")
run_command(ssh, "rm -rf /usr/share/nginx/html/*")
run_command(ssh, "cp -r /opt/anime-website/dist/* /usr/share/nginx/html/")
run_command(ssh, "chown -R nginx:nginx /usr/share/nginx/html/")

# 6. 重启Nginx
print("\n=== 6. 重启Nginx ===")
run_command(ssh, "systemctl restart nginx")

# 7. 测试前端访问
print("\n=== 7. 测试前端访问 ===")
out, err = run_command(ssh, "curl -s http://localhost | head -20")
print(out[:500])

# 8. 测试API访问
print("\n=== 8. 测试API访问 ===")
out, err = run_command(ssh, "curl -s http://localhost/api/health")
print("健康检查:", out)
out, err = run_command(ssh, "curl -s http://localhost/api/animes?page=1&limit=1")
print("动漫数据:", out[:200])

ssh.close()

print("\n" + "="*60)
print("前端API地址更新完成！")
print("="*60)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在前端使用相对路径访问API，不再依赖localhost")
print("="*60)
