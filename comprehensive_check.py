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
print("全面检查所有服务状态")
print("="*70)

# 1. 检查后端服务
print("\n=== 1. 后端服务状态 ===")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print("后端状态:", out.strip())

out, err = run_command(ssh, "pm2 logs anime-backend --lines 20 --nostream 2>&1 | tail -30")
print("后端日志:", out[:500])

# 2. 检查Nginx服务
print("\n=== 2. Nginx服务状态 ===")
out, err = run_command(ssh, "systemctl is-active nginx")
print("Nginx状态:", out.strip())

out, err = run_command(ssh, "nginx -t 2>&1")
print("Nginx配置测试:", out)

# 3. 检查MySQL服务
print("\n=== 3. MySQL服务状态 ===")
out, err = run_command(ssh, "systemctl is-active mysqld")
print("MySQL状态:", out.strip())

out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) as total FROM anime_db.animes;' 2>&1")
print("数据库动漫数量:", out)

# 4. 检查端口占用
print("\n=== 4. 端口占用检查 ===")
out, err = run_command(ssh, "netstat -tlnp | grep -E '3001|80|3306'")
print("端口状态:", out)

# 5. 测试后端API（直接访问）
print("\n=== 5. 测试后端API（直接访问） ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("健康检查:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/anime?page=1&limit=1 2>&1")
print("动漫数据:", out[:200])

# 6. 测试Nginx API（通过代理）
print("\n=== 6. 测试Nginx API（通过代理） ===")
out, err = run_command(ssh, "curl -s http://localhost/api/health 2>&1")
print("健康检查:", out)

out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1 2>&1")
print("动漫数据:", out[:200])

# 7. 检查前端文件
print("\n=== 7. 前端文件检查 ===")
out, err = run_command(ssh, "ls -la /usr/share/nginx/html/")
print("前端文件:", out)

out, err = run_command(ssh, "cat /usr/share/nginx/html/index.html | head -10")
print("index.html头部:", out[:300])

# 8. 检查Nginx配置
print("\n=== 8. Nginx配置检查 ===")
out, err = run_command(ssh, "cat /etc/nginx/nginx.conf | grep -A 20 'location /api/'")
print("API代理配置:", out)

# 9. 检查防火墙
print("\n=== 9. 防火墙检查 ===")
out, err = run_command(ssh, "firewall-cmd --list-ports 2>&1")
print("开放端口:", out)

# 10. 检查Nginx错误日志
print("\n=== 10. Nginx错误日志 ===")
out, err = run_command(ssh, "tail -20 /var/log/nginx/error.log 2>&1")
print("错误日志:", out[:500])

ssh.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
