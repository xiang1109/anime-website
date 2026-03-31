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

print("=== 最终测试 ===")

# 1. 测试后端API
print("\n1. 后端API测试:")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health")
print("   /api/health:", out[:50])

out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime?page=1&limit=2' 2>/dev/null | head -100")
print("   /api/anime:", out[:150])

# 2. 通过Nginx测试API
print("\n2. Nginx代理测试:")
out, err = run_command(ssh, "curl -s http://localhost/api/health")
print("   /api/health (through Nginx):", out[:50])

# 3. 测试前端页面
print("\n3. 前端页面测试:")
out, err = run_command(ssh, "curl -s http://localhost/ | grep -i '<title>'")
print("   页面标题:", out.strip())

# 4. 检查服务状态
print("\n4. 服务状态:")
out, err = run_command(ssh, "pm2 status anime-backend")
print(out)

ssh.close()

print("\n=== 部署完成！===")
print(f"🌐 网站访问地址: http://{hostname}")
print(f"🔧 后端API地址: http://{hostname}/api")
print(f"👑 管理员账号: admin / admin123")
print("\n功能包括:")
print("  - 用户注册/登录")
print("  - 动漫搜索和浏览")
print("  - 动漫详情和评分")
print("  - 管理员后台管理(增删改查)")
