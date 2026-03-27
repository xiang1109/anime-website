import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("=== 1. 检查MySQL状态 ===")
out, err = run_command(ssh, "systemctl status mysqld | head -15")
print(out)

print("\n=== 2. 检查端口监听 ===")
out, err = run_command(ssh, "ss -tlnp | grep -E '80|3001|3306'")
print(out)

print("\n=== 3. 测试本地访问 ===")
out, err = run_command(ssh, "curl -s -w '\\nHTTP Code: %{http_code}\\n' http://localhost/")
print("前端访问:", out)

out, err = run_command(ssh, "curl -s -w '\\nHTTP Code: %{http_code}\\n' http://localhost/api/health")
print("API健康检查:", out)

out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?limit=1' | head -80")
print("动漫列表:", out[:150])

print("\n=== 4. 检查防火墙 ===")
out, err = run_command(ssh, "systemctl status firewalld | head -5")
print(out)
out, err = run_command(ssh, "firewall-cmd --list-all 2>/dev/null | head -20 || echo 'firewalld not active'")
print(out)

print("\n=== 5. 检查Nginx配置 ===")
out, err = run_command(ssh, "cat /etc/nginx/conf.d/anime-website.conf")
print(out)

print("\n=== 6. 检查Nginx错误日志 ===")
out, err = run_command(ssh, "tail -20 /var/log/nginx/error.log 2>/dev/null")
print(out)

ssh.close()
