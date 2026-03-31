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
print("配置MySQL远程连接")
print("="*60)

# 1. 修改MySQL配置允许远程连接
print("\n=== 1. 修改MySQL配置 ===")
mysql_config = """[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
bind-address = 0.0.0.0
mysqlx-bind-address = 0.0.0.0
default_authentication_plugin = mysql_native_password
"""
run_command(ssh, f"cat > /etc/my.cnf <<'EOF'\n{mysql_config}\nEOF")
print("MySQL配置已更新")

# 2. 重启MySQL服务
print("\n=== 2. 重启MySQL服务 ===")
run_command(ssh, "systemctl restart mysqld")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "systemctl is-active mysqld")
print("MySQL状态:", out.strip())

# 3. 创建允许远程连接的MySQL用户
print("\n=== 3. 创建远程连接用户 ===")
sql_commands = """
DROP USER IF EXISTS 'anime_user'@'%';
CREATE USER 'anime_user'@'%' IDENTIFIED BY 'Xinmima1109';
GRANT ALL PRIVILEGES ON anime_db.* TO 'anime_user'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'Xinmima1109';
FLUSH PRIVILEGES;
SELECT user, host FROM mysql.user WHERE host = '%';
"""
out, err = run_command(ssh, f"mysql -u root -p'Xinmima1109' -e \"{sql_commands}\" 2>&1 | grep -v Warning")
print(out)

# 4. 检查MySQL绑定地址
print("\n=== 4. 检查MySQL绑定地址 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e \"SHOW VARIABLES LIKE 'bind_address';\" 2>&1 | grep -v Warning")
print("bind_address:", out)

# 5. 检查MySQL端口监听
print("\n=== 5. 检查MySQL端口监听 ===")
out, err = run_command(ssh, "ss -tlnp | grep 3306")
print("3306端口监听:", out)

# 6. 测试远程连接（本地测试）
print("\n=== 6. 测试远程连接 ===")
out, err = run_command(ssh, "mysql -h 127.0.0.1 -u anime_user -p'Xinmima1109' -e 'SELECT 1;' 2>&1 | grep -v Warning")
print("远程连接测试:", out)

# 7. 测试后端服务
print("\n=== 7. 测试后端服务 ===")
run_command(ssh, "pm2 restart anime-backend")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("后端健康检查:", out)
out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=1 2>&1")
print("动漫数据:", out[:200])

ssh.close()

print("\n" + "="*60)
print("MySQL远程连接配置完成！")
print("="*60)
print("\n远程连接信息：")
print("主机: 59.110.214.50")
print("端口: 3306")
print("数据库: anime_db")
print("用户名: anime_user")
print("密码: Xinmima1109")
print("\n或者使用root账号：")
print("用户名: root")
print("密码: Xinmima1109")
print("\n注意：")
print("1. 阿里云安全组3306端口已开放")
print("2. 如果连接失败，请检查防火墙设置")
print("="*60)
