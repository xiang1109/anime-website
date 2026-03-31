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

# 1. 检查MySQL配置
print("\n=== 1. 检查MySQL配置 ===")
out, err = run_command(ssh, "cat /etc/my.cnf")
print(out)

# 2. 修改MySQL配置允许远程连接
print("\n=== 2. 修改MySQL配置 ===")
mysql_config = """[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
bind-address = 0.0.0.0
default_authentication_plugin = mysql_native_password
"""
run_command(ssh, f"cat > /etc/my.cnf <<'EOF'\n{mysql_config}\nEOF")
print("MySQL配置已更新")

# 3. 重启MySQL服务
print("\n=== 3. 重启MySQL服务 ===")
run_command(ssh, "systemctl restart mysqld")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "systemctl is-active mysqld")
print("MySQL状态:", out.strip())

# 4. 创建允许远程连接的MySQL用户
print("\n=== 4. 创建远程连接用户 ===")
sql_commands = """
CREATE USER IF NOT EXISTS 'anime_user'@'%' IDENTIFIED BY 'Xinmima1109';
GRANT ALL PRIVILEGES ON anime_db.* TO 'anime_user'@'%';
FLUSH PRIVILEGES;
SELECT user, host FROM mysql.user WHERE user = 'anime_user';
"""
out, err = run_command(ssh, f"mysql -u root -p'Xinmima1109' -e \"{sql_commands}\" 2>&1 | grep -v Warning")
print(out)

# 5. 开放防火墙3306端口
print("\n=== 5. 开放防火墙3306端口 ===")
run_command(ssh, "firewall-cmd --permanent --add-port=3306/tcp 2>&1 || true")
run_command(ssh, "firewall-cmd --reload 2>&1 || true")
out, err = run_command(ssh, "firewall-cmd --list-ports 2>&1 || true")
print("开放端口:", out)

# 6. 检查阿里云安全组是否开放3306端口
print("\n=== 6. 检查阿里云安全组 ===")
out, err = run_command(ssh, "aliyun ecs DescribeSecurityGroups --RegionId cn-beijing 2>&1 | head -50")
print(out[:1000])

# 7. 获取安全组ID
print("\n=== 7. 获取安全组ID ===")
out, err = run_command(ssh, "aliyun ecs DescribeInstances --RegionId cn-beijing 2>&1 | grep -A5 'SecurityGroupId' | head -10")
print(out)

# 8. 开放3306端口
print("\n=== 8. 开放3306端口 ===")
out, err = run_command(ssh, "aliyun ecs DescribeInstances --RegionId cn-beijing 2>&1 | grep -o 'sg-[a-zA-Z0-9]*' | head -1")
sg_id = out.strip()
if sg_id:
    print(f"安全组ID: {sg_id}")
    cmd = f"""aliyun ecs AuthorizeSecurityGroup --RegionId cn-beijing --SecurityGroupId {sg_id} --IpProtocol tcp --PortRange "3306/3306" --SourceCidrIp "0.0.0.0/0" --Policy accept --Description "MySQL" 2>&1"""
    out, err = run_command(ssh, cmd)
    print(out)
else:
    print("无法获取安全组ID，请手动在阿里云控制台开放3306端口")

# 9. 验证MySQL远程连接
print("\n=== 9. 验证MySQL远程连接 ===")
out, err = run_command(ssh, "ss -tlnp | grep 3306")
print("3306端口监听:", out)

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
print("\n注意：如果连接失败，请在阿里云控制台安全组手动开放3306端口")
print("="*60)
