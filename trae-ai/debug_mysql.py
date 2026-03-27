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
print("调试MySQL问题")
print("="*60)

# 1. 检查MySQL错误日志位置
print("\n=== 1. 查找MySQL错误日志 ===")
out, err = run_command(ssh, "find /var/log -name '*.log' | grep -i mysql 2>/dev/null | head -10")
print(out)

out, err = run_command(ssh, "ls -la /var/log/ | grep -i mysql 2>/dev/null")
print(out)

# 2. 检查MySQL数据目录
print("\n=== 2. 检查MySQL数据目录 ===")
out, err = run_command(ssh, "ls -la /var/lib/mysql/ | head -20")
print(out)

# 3. 检查MySQL配置文件
print("\n=== 3. 检查MySQL配置文件 ===")
out, err = run_command(ssh, "cat /etc/my.cnf")
print(out)

# 4. 检查MySQL系统日志
print("\n=== 4. 检查MySQL系统日志 ===")
out, err = run_command(ssh, "journalctl -u mysqld --no-pager | tail -50")
print(out)

# 5. 检查MySQL错误日志文件
print("\n=== 5. 检查MySQL错误日志文件 ===")
out, err = run_command(ssh, "ls -la /var/lib/mysql/*.err 2>/dev/null | head -5")
print(out)

# 6. 尝试查看错误日志内容
print("\n=== 6. 查看错误日志内容 ===")
out, err = run_command(ssh, "cat /var/lib/mysql/*.err 2>/dev/null | tail -50")
print(out)

# 7. 尝试手动启动MySQL
print("\n=== 7. 手动启动MySQL ===")
out, err = run_command(ssh, "mysqld --verbose --help 2>&1 | head -20")
print(out[:500])

# 8. 检查MySQL权限
print("\n=== 8. 检查MySQL权限 ===")
out, err = run_command(ssh, "ls -la /var/lib/mysql/ | head -10")
print(out)

# 9. 修复MySQL权限
print("\n=== 9. 修复MySQL权限 ===")
run_command(ssh, "chown -R mysql:mysql /var/lib/mysql/")
run_command(ssh, "chmod -R 755 /var/lib/mysql/")
print("权限已修复")

# 10. 重新初始化MySQL（如果需要）
print("\n=== 10. 检查是否需要重新初始化 ===")
out, err = run_command(ssh, "ls -la /var/lib/mysql/mysql/ 2>/dev/null | head -5")
print(out)

if "No such file or directory" in out:
    print("需要重新初始化MySQL...")
    run_command(ssh, "mysqld --initialize --user=mysql 2>&1")
    run_command(ssh, "sleep 5")
else:
    print("MySQL数据目录已存在")

# 11. 尝试启动MySQL
print("\n=== 11. 尝试启动MySQL ===")
run_command(ssh, "systemctl stop mysqld 2>&1 || true")
run_command(ssh, "sleep 2")
run_command(ssh, "systemctl start mysqld 2>&1")
run_command(ssh, "sleep 5")
out, err = run_command(ssh, "systemctl is-active mysqld")
print("MySQL状态:", out.strip())

ssh.close()
