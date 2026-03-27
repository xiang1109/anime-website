import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    print(f"\n=== {command} ===")
    print(out)
    if err:
        print("STDERR:", err)
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

# 检查MySQL状态
run_command(ssh, "systemctl status mysqld | head -30")
run_command(ssh, "netstat -tlnp | grep mysql")
run_command(ssh, "ps aux | grep mysqld")

# 测试MySQL连接
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT 1'")

# 检查MySQL绑定地址
run_command(ssh, "grep bind-address /etc/my.cnf /etc/my.cnf.d/*.cnf 2>/dev/null")

ssh.close()
