import paramiko
import time

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
print("修复MySQL服务")
print("="*60)

# 1. 检查MySQL状态
print("\n=== 1. 检查MySQL状态 ===")
out, err = run_command(ssh, "systemctl status mysqld 2>&1 | head -30")
print(out)

# 2. 恢复原始MySQL配置
print("\n=== 2. 恢复原始MySQL配置 ===")
mysql_config = """[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
"""
run_command(ssh, f"cat > /etc/my.cnf <<'EOF'\n{mysql_config}\nEOF")
print("MySQL配置已恢复")

# 3. 重新启动MySQL
print("\n=== 3. 重新启动MySQL ===")
run_command(ssh, "systemctl stop mysqld 2>&1 || true")
run_command(ssh, "sleep 2")
run_command(ssh, "systemctl start mysqld 2>&1")
run_command(ssh, "sleep 5")
out, err = run_command(ssh, "systemctl is-active mysqld")
print("MySQL状态:", out.strip())

# 4. 检查MySQL日志
print("\n=== 4. 检查MySQL错误日志 ===")
out, err = run_command(ssh, "tail -30 /var/log/mysqld.log 2>&1 | head -30")
print(out)

# 5. 创建允许远程连接的MySQL用户
print("\n=== 5. 创建远程连接用户 ===")
sql_commands = """
CREATE USER IF NOT EXISTS 'anime_user'@'%' IDENTIFIED BY 'Xinmima1109';
GRANT ALL PRIVILEGES ON anime_db.* TO 'anime_user'@'%';
FLUSH PRIVILEGES;
SELECT user, host FROM mysql.user WHERE user = 'anime_user';
"""
out, err = run_command(ssh, f"mysql -u root -p'Xinmima1109' -e \"{sql_commands}\" 2>&1 | grep -v Warning")
print(out)

# 6. 检查MySQL端口监听
print("\n=== 6. 检查MySQL端口监听 ===")
out, err = run_command(ssh, "ss -tlnp | grep 3306")
print("3306端口监听:", out)

# 7. 修改MySQL绑定地址为0.0.0.0
print("\n=== 7. 修改MySQL绑定地址 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e \"SHOW VARIABLES LIKE 'bind_address';\" 2>&1 | grep -v Warning")
print("当前bind_address:", out)

# 8. 测试后端服务
print("\n=== 8. 测试后端服务 ===")
run_command(ssh, "pm2 restart anime-backend")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("后端健康检查:", out)
out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=1 2>&1")
print("动漫数据:", out[:300])

ssh.close()

print("\n" + "="*60)
print("MySQL服务修复完成！")
print("="*60)
print("\n远程连接信息：")
print("主机: 59.110.214.50")
print("端口: 3306")
print("数据库: anime_db")
print("用户名: anime_user")
print("密码: Xinmima1109")
print("\n注意：MySQL默认只监听localhost，需要修改配置才能远程连接")
print("如果你需要远程连接，请执行下一步配置")
print("="*60)
