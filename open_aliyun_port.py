import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("="*60)
print("检查阿里云CLI和安全组配置")
print("="*60)

# 检查是否安装了阿里云CLI
out, err = run_command(ssh, "which aliyun 2>/dev/null || echo 'not installed'")
print(f"阿里云CLI: {out.strip()}")

# 检查服务器的安全组信息
print("\n=== 服务器元数据 ===")
out, err = run_command(ssh, "curl -s http://100.100.100.200/latest/meta-data/instance-id 2>/dev/null")
print(f"实例ID: {out[:50]}")

out, err = run_command(ssh, "curl -s http://100.100.100.200/latest/meta-data/region-id 2>/dev/null")
print(f"地域: {out}")

# 检查是否可以访问阿里云API
out, err = run_command(ssh, "curl -s --connect-timeout 3 https://ecs.aliyuncs.com 2>&1 | head -5")
print(f"\n阿里云API访问: {out[:100]}")

# 检查iptables规则（服务器防火墙）
print("\n=== 服务器防火墙规则 ===")
out, err = run_command(ssh, "iptables -L INPUT -n -v | head -15")
print(out)

ssh.close()

print("\n" + "="*60)
print("解决方案：手动在阿里云控制台开放80端口")
print("="*60)
print("\n请按以下步骤操作：")
print("\n1. 登录阿里云控制台：https://ecs.console.aliyun.com/")
print("2. 找到你的ECS实例（IP: 59.110.214.50）")
print("3. 点击实例ID进入详情页")
print("4. 点击左侧菜单的「安全组」")
print("5. 点击「配置规则」按钮")
print("6. 点击「添加安全组规则」")
print("7. 填写以下信息：")
print("   - 规则方向：入方向")
print("   - 授权策略：允许")
print("   - 协议类型：TCP")
print("   - 端口范围：80/80")
print("   - 授权对象：0.0.0.0/0")
print("   - 描述：HTTP")
print("8. 点击「保存」")
print("\n配置完成后，等待1-2分钟，然后访问：http://59.110.214.50")
print("="*60)
