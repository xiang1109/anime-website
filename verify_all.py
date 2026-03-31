import paramiko
import time

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

print("=== 后端服务状态 ===")
out, err = run_command(ssh, "pm2 status")
print(out)

print("\n=== 测试后端API ===")
out, err = run_command(ssh, "sleep 2 && curl -s http://localhost:3001/api/health")
print("健康检查:", out.strip())

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?limit=1")
print("动漫列表:", out[:200])

print("\n=== Nginx状态 ===")
out, err = run_command(ssh, "systemctl status nginx | head -15")
print(out)

# 检查前端文件是否存在
print("\n=== 前端文件检查 ===")
out, err = run_command(ssh, "ls -la /opt/anime-website/frontend/ | head -10")
print(out)

# 测试Nginx代理
print("\n=== 测试Nginx代理 ===")
out, err = run_command(ssh, "curl -s http://localhost/api/health")
print("API通过Nginx:", out.strip())

ssh.close()

print(f"\n=== 部署完成！===")
print(f"网站访问地址: http://{hostname}")
print(f"后端API地址: http://{hostname}/api")
print(f"管理员账号: admin / admin123")
