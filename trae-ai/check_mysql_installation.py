import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show=True):
    if show:
        print(f"\n执行: {command[:80]}...")
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
print("检查MySQL安装状态")
print("="*60)

# 1. 检查MySQL服务状态
print("\n=== 1. MySQL服务状态 ===")
out, err = run_command(ssh, "systemctl status mysqld | grep -E 'Active|PID|Loaded'")
print(out)

# 2. 检查MySQL版本
print("\n=== 2. MySQL版本 ===")
out, err = run_command(ssh, "mysql --version")
print(out)

# 3. 检查MySQL安装路径
print("\n=== 3. MySQL安装路径 ===")
out, err = run_command(ssh, "which mysql")
print(out)

# 4. 检查MySQL配置文件
print("\n=== 4. MySQL配置文件 ===")
out, err = run_command(ssh, "ls -la /etc/my.cnf /etc/mysql/ 2>/dev/null | head -10")
print(out)

# 5. 检查MySQL数据目录
print("\n=== 5. MySQL数据目录 ===")
out, err = run_command(ssh, "ls -la /var/lib/mysql/ | head -10")
print(out)

# 6. 检查数据库
print("\n=== 6. 数据库列表 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SHOW DATABASES;' 2>&1 | grep -v Warning")
print(out)

# 7. 检查动漫数据
print("\n=== 7. 动漫数据 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' anime_db -e 'SELECT COUNT(*) FROM animes;' 2>&1 | grep -v Warning")
print(f"动漫数量: {out.strip()}")

ssh.close()

print("\n" + "="*60)
print("MySQL已安装在阿里云服务器上！")
print("="*60)
print("主机: localhost (阿里云服务器本地)")
print("数据库: anime_db")
print("用户名: root")
print("密码: Xinmima1109")
print("="*60)
