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

# 检查iptables规则
run_command(ssh, "iptables -L -n | head -30")

# 检查是否有其他防火墙
run_command(ssh, "which firewall-cmd ufw iptables 2>/dev/null")

# 尝试开放80端口
print("\n=== 尝试开放80端口 ===")
run_command(ssh, "iptables -I INPUT -p tcp --dport 80 -j ACCEPT")
run_command(ssh, "iptables -I INPUT -p tcp --dport 3001 -j ACCEPT")
run_command(ssh, "iptables-save | head -20")

# 检查SELinux状态
run_command(ssh, "getenforce 2>/dev/null || echo 'SELinux not available'")

ssh.close()

print("\n" + "="*60)
print("问题诊断：阿里云安全组80端口未开放")
print("解决方案：")
print("1. 登录阿里云控制台")
print("2. 找到ECS实例 -> 安全组")
print("3. 添加安全组规则：TCP 80端口 0.0.0.0/0")
print("4. 或者临时测试可以用：ssh -L 8080:localhost:80 root@59.110.214.50")
print("   然后访问 http://localhost:8080")
print("="*60)
