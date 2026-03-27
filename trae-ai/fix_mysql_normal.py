import paramiko
import time

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    print(f"\n执行: {command[:60]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if out:
        print(out)
    if err:
        print("STDERR:", err)
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("=== 重启MySQL到正常模式 ===")

# 杀掉当前mysqld进程并正常启动
run_command(ssh, "pkill -9 mysqld && sleep 3")
run_command(ssh, "rm -f /var/lib/mysql/mysql.sock.lock")
run_command(ssh, "systemctl start mysqld && sleep 10")

# 检查状态
run_command(ssh, "systemctl status mysqld | head -20")
run_command(ssh, "netstat -tlnp | grep :3306")

# 测试连接
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT 1'")

ssh.close()
