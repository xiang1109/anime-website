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
print("尝试使用阿里云CLI自动开放80端口")
print("="*60)

# 获取实例信息
out, err = run_command(ssh, "curl -s http://100.100.100.200/latest/meta-data/instance-id")
instance_id = out.strip()
print(f"实例ID: {instance_id}")

out, err = run_command(ssh, "curl -s http://100.100.100.200/latest/meta-data/region-id")
region = out.strip()
print(f"地域: {region}")

# 检查阿里云CLI配置
out, err = run_command(ssh, "aliyun configure list 2>&1 | head -10")
print("\n阿里云CLI配置:")
print(out)

# 尝试获取安全组ID
print("\n=== 获取安全组信息 ===")
out, err = run_command(ssh, f"aliyun ecs DescribeInstances --InstanceIds '[\"{instance_id}\"]' --RegionId {region} 2>&1")
print(out[:500])

if "SecurityGroupId" in out:
    # 提取安全组ID
    import json
    try:
        data = json.loads(out)
        sg_id = data['Instances']['Instance'][0]['SecurityGroupIds']['SecurityGroupId'][0]
        print(f"\n找到安全组ID: {sg_id}")
        
        # 添加入方向规则
        print("\n=== 添加80端口规则 ===")
        cmd = f"""aliyun ecs AuthorizeSecurityGroup --RegionId {region} --SecurityGroupId {sg_id} --IpProtocol tcp --PortRange 80/80 --SourceCidrIp 0.0.0.0/0 --Policy accept --Description HTTP 2>&1"""
        out, err = run_command(ssh, cmd)
        print(out)
        
        if "RequestId" in out:
            print("\n✅ 80端口已成功开放！")
            print("等待1-2分钟后访问: http://59.110.214.50")
        else:
            print("\n❌ 添加规则失败，请手动在阿里云控制台操作")
    except Exception as e:
        print(f"解析错误: {e}")
        print("\n请手动在阿里云控制台操作")
else:
    print("\n无法自动获取安全组信息")
    print("\n请按以下步骤手动操作：")

print("\n" + "="*60)
print("手动操作步骤（如果自动失败）：")
print("1. 登录：https://ecs.console.aliyun.com/")
print(f"2. 找到实例：{instance_id}")
print("3. 安全组 -> 配置规则 -> 添加安全组规则")
print("4. TCP 80/80  0.0.0.0/0")
print("5. 保存后访问：http://59.110.214.50")
print("="*60)

ssh.close()
