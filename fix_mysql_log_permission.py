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
print("修复MySQL日志文件权限问题")
print("="*60)

# 1. 创建并修复日志文件权限
print("\n=== 1. 创建并修复日志文件权限 ===")
run_command(ssh, "touch /var/log/mysqld.log")
run_command(ssh, "chown mysql:mysql /var/log/mysqld.log")
run_command(ssh, "chmod 644 /var/log/mysqld.log")
print("日志文件权限已修复")

# 2. 检查MySQL配置文件
print("\n=== 2. 检查MySQL配置文件 ===")
out, err = run_command(ssh, "cat /etc/my.cnf")
print(out)

# 3. 确保配置文件正确
print("\n=== 3. 更新MySQL配置文件 ===")
mysql_config = """[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
"""
run_command(ssh, f"cat > /etc/my.cnf <<'EOF'\n{mysql_config}\nEOF")
print("MySQL配置已更新")

# 4. 创建pid目录
print("\n=== 4. 创建pid目录 ===")
run_command(ssh, "mkdir -p /var/run/mysqld")
run_command(ssh, "chown mysql:mysql /var/run/mysqld")
run_command(ssh, "chmod 755 /var/run/mysqld")
print("pid目录已创建")

# 5. 修复所有权限
print("\n=== 5. 修复所有MySQL相关权限 ===")
run_command(ssh, "chown -R mysql:mysql /var/lib/mysql/")
run_command(ssh, "chmod -R 755 /var/lib/mysql/")
print("所有权限已修复")

# 6. 停止MySQL（如果还在运行）
print("\n=== 6. 停止MySQL服务 ===")
run_command(ssh, "systemctl stop mysqld 2>&1 || true")
run_command(ssh, "pkill -9 mysqld 2>&1 || true")
run_command(ssh, "sleep 2")

# 7. 启动MySQL
print("\n=== 7. 启动MySQL服务 ===")
run_command(ssh, "systemctl start mysqld 2>&1")
run_command(ssh, "sleep 5")

# 8. 检查MySQL状态
print("\n=== 8. 检查MySQL状态 ===")
out, err = run_command(ssh, "systemctl is-active mysqld")
print("MySQL状态:", out.strip())

# 9. 检查MySQL错误日志
print("\n=== 9. 检查MySQL错误日志 ===")
out, err = run_command(ssh, "tail -20 /var/log/mysqld.log 2>&1")
print(out)

# 10. 测试MySQL连接
print("\n=== 10. 测试MySQL连接 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT 1;' 2>&1 | grep -v Warning")
print("连接测试:", out)

# 11. 测试后端服务
print("\n=== 11. 测试后端服务 ===")
run_command(ssh, "pm2 restart anime-backend")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("后端健康检查:", out)
out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=1 2>&1")
print("动漫数据:", out[:300])

ssh.close()

print("\n" + "="*60)
print("MySQL修复完成！")
print("="*60)
