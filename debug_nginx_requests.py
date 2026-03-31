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
print("调试Nginx请求")
print("="*70)

# 1. 清除Nginx日志
print("\n=== 1. 清除Nginx日志 ===")
run_command(ssh, "echo '' > /var/log/nginx/access.log")
run_command(ssh, "echo '' > /var/log/nginx/error.log")

# 2. 发送测试请求
print("\n=== 2. 发送测试请求 ===")
out, err = run_command(ssh, "curl -v http://localhost/api/health 2>&1")
print(out[:500])

# 3. 查看访问日志
print("\n=== 3. 查看访问日志 ===")
out, err = run_command(ssh, "cat /var/log/nginx/access.log")
print(out)

# 4. 查看错误日志
print("\n=== 4. 查看错误日志 ===")
out, err = run_command(ssh, "cat /var/log/nginx/error.log")
print(out)

# 5. 检查Nginx进程
print("\n=== 5. 检查Nginx进程 ===")
out, err = run_command(ssh, "ps aux | grep nginx | grep -v grep")
print(out)

# 6. 强制重启Nginx
print("\n=== 6. 强制重启Nginx ===")
run_command(ssh, "systemctl stop nginx")
run_command(ssh, "sleep 1")
run_command(ssh, "systemctl start nginx")
run_command(ssh, "sleep 1")

# 7. 再次测试
print("\n=== 7. 再次测试 ===")
out, err = run_command(ssh, "curl -v http://localhost/api/health 2>&1")
print(out[:500])

# 8. 查看最新日志
print("\n=== 8. 查看最新日志 ===")
out, err = run_command(ssh, "tail -10 /var/log/nginx/access.log")
print("访问日志:", out)
out, err = run_command(ssh, "tail -10 /var/log/nginx/error.log")
print("错误日志:", out)

ssh.close()

print("\n" + "="*70)
print("调试完成")
print("="*70)
