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
print("重新部署前端")
print("="*60)

# 1. 检查Nginx配置
print("\n=== 1. 检查Nginx配置 ===")
out, err = run_command(ssh, "cat /etc/nginx/nginx.conf")
print(out)

# 2. 重新上传前端代码
print("\n=== 2. 重新上传前端代码 ===")
run_command(ssh, "rm -rf /opt/anime-website/src")
run_command(ssh, "mkdir -p /opt/anime-website/src")
run_command(ssh, "cd /opt/anime-website && npm run build 2>&1 | tail -20")

# 3. 复制构建产物到Nginx
print("\n=== 3. 复制构建产物到Nginx ===")
run_command(ssh, "rm -rf /usr/share/nginx/html/*")
run_command(ssh, "cp -r /opt/anime-website/dist/* /usr/share/nginx/html/")
run_command(ssh, "chown -R nginx:nginx /usr/share/nginx/html/")

# 4. 重启Nginx
print("\n=== 4. 重启Nginx ===")
run_command(ssh, "systemctl restart nginx")

# 5. 测试前端访问
print("\n=== 5. 测试前端访问 ===")
out, err = run_command(ssh, "curl -s http://localhost | head -20")
print(out[:500])

# 6. 测试API访问
print("\n=== 6. 测试API访问 ===")
out, err = run_command(ssh, "curl -s http://localhost/api/health")
print("健康检查:", out)
out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1")
print("动漫数据:", out[:200])

ssh.close()

print("\n" + "="*60)
print("前端重新部署完成！")
print("="*60)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("="*60)
