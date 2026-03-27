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
print("验证简单HTML页面")
print("="*60)

# 1. 检查Nginx配置
print("\n=== 1. 检查Nginx配置 ===")
out, err = run_command(ssh, "cat /etc/nginx/nginx.conf")
print(out)

# 2. 检查index.html内容
print("\n=== 2. 检查index.html内容 ===")
out, err = run_command(ssh, "cat /usr/share/nginx/html/index.html | head -30")
print(out[:500])

# 3. 测试页面访问
print("\n=== 3. 测试页面访问 ===")
out, err = run_command(ssh, "curl -s -o /dev/null -w '%{http_code}' http://localhost 2>&1")
print("HTTP状态码:", out.strip())

# 4. 测试API
print("\n=== 4. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1")
print("API响应:", out[:200])

# 5. 检查所有服务状态
print("\n=== 5. 检查所有服务状态 ===")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print("后端:", out.strip())

out, err = run_command(ssh, "systemctl is-active nginx")
print("Nginx:", out.strip())

out, err = run_command(ssh, "systemctl is-active mysqld")
print("MySQL:", out.strip())

ssh.close()

print("\n" + "="*60)
print("验证完成！")
print("="*60)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n如果仍然看不到数据，请打开浏览器开发者工具（F12）查看Console和Network标签页的错误信息")
print("="*60)
