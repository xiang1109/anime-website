import paramiko
import json

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
print("尝试使用阿里云API开放80端口")
print("="*60)

# 1. 测试获取实例信息
print("\n=== 1. 测试获取实例信息 ===")
out, err = run_command(ssh, "aliyun ecs DescribeInstances --InstanceIds '[\"i-2zebnofeue7gp6wo1d15\"]' --RegionId cn-beijing 2>&1")
print(out[:800])

if "ErrorCode" in out:
    print("\n❌ 仍然没有权限，请确认已给子账号授权ECS权限")
    ssh.close()
    exit(1)

# 2. 解析安全组ID
try:
    data = json.loads(out)
    sg_id = data['Instances']['Instance'][0]['SecurityGroupIds']['SecurityGroupId'][0]
    print(f"\n✅ 找到安全组ID: {sg_id}")
except Exception as e:
    print(f"\n❌ 解析安全组ID失败: {e}")
    ssh.close()
    exit(1)

# 3. 检查现有安全组规则
print("\n=== 3. 检查现有安全组规则 ===")
out, err = run_command(ssh, f"aliyun ecs DescribeSecurityGroupAttribute --RegionId cn-beijing --SecurityGroupId {sg_id} 2>&1")
print(out[:1000])

# 4. 添加80端口规则
print("\n=== 4. 添加80端口规则 ===")
cmd = f"""aliyun ecs AuthorizeSecurityGroup --RegionId cn-beijing --SecurityGroupId {sg_id} --IpProtocol tcp --PortRange "80/80" --SourceCidrIp "0.0.0.0/0" --Policy accept --Description "HTTP" 2>&1"""
out, err = run_command(ssh, cmd)
print(out)

if "RequestId" in out:
    print("\n✅ 80端口已成功开放！")
    print("等待1-2分钟后访问: http://59.110.214.50")
else:
    print("\n❌ 添加规则失败，请检查错误信息")

ssh.close()

print("\n" + "="*60)
print("操作完成！")
print("="*60)
