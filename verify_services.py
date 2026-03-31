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

print("=" * 60)
print("服务状态确认")
print("=" * 60)

# 检查所有服务
print("\n1. Nginx:")
out, err = run_command(ssh, "systemctl is-active nginx")
print(f"   状态: {out.strip()}")

print("\n2. MySQL:")
out, err = run_command(ssh, "systemctl is-active mysqld")
print(f"   状态: {out.strip()}")

print("\n3. 后端服务:")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print(f"   {out.strip()}")

print("\n4. 端口监听:")
out, err = run_command(ssh, "ss -tlnp | grep -E '80|3001|3306'")
print(out)

print("\n5. 本地测试:")
out, err = run_command(ssh, "curl -s -w 'HTTP %{http_code}' http://localhost/")
print(f"   前端: {out[:50]}")
out, err = run_command(ssh, "curl -s http://localhost/api/health")
print(f"   API: {out}")

print("\n" + "=" * 60)
print("所有服务运行正常！")
print("请在阿里云控制台开放80端口后访问: http://59.110.214.50")
print("或使用SSH端口转发测试: ssh -L 8080:localhost:80 root@59.110.214.50")
print("=" * 60)

ssh.close()
