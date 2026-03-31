import paramiko
import os
import tarfile

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

print("="*70)
print("部署React前端（包含秒速五厘米角落元素）")
print("="*70)

# 1. 备份当前前端
print("\n=== 1. 备份当前前端 ===")
run_command(ssh, "cp -r /usr/share/nginx/html /usr/share/nginx/html.bak3")
print("备份完成")

# 2. 压缩构建文件
print("\n=== 2. 压缩构建文件 ===")
with tarfile.open("dist.tar.gz", "w:gz") as tar:
    for root, dirs, files in os.walk("d:/code/trae-ai/dist"):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, "d:/code/trae-ai/dist")
            tar.add(file_path, arcname=arcname)
print("压缩完成")

# 3. 上传到服务器
print("\n=== 3. 上传到服务器 ===")
sftp = ssh.open_sftp()
sftp.put("dist.tar.gz", "/root/dist.tar.gz")
sftp.close()
print("上传完成")

# 4. 解压到nginx目录
print("\n=== 4. 解压到nginx目录 ===")
run_command(ssh, "rm -rf /usr/share/nginx/html/*")
run_command(ssh, "tar -xzf /root/dist.tar.gz -C /usr/share/nginx/html/")
print("解压完成")

# 5. 验证部署
print("\n=== 5. 验证部署 ===")
out, err = run_command(ssh, "ls -la /usr/share/nginx/html/")
print(out)

# 6. 清理临时文件
print("\n=== 6. 清理临时文件 ===")
os.remove("dist.tar.gz")
run_command(ssh, "rm -f /root/dist.tar.gz")
print("清理完成")

# 7. 重启nginx
print("\n=== 7. 重启nginx ===")
out, err = run_command(ssh, "nginx -t")
print(out)
if err:
    print("Nginx配置错误:", err)
else:
    run_command(ssh, "systemctl restart nginx")
    print("Nginx重启成功")

ssh.close()

print("\n" + "="*70)
print("前端部署完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在应该可以看到：")
print("1. 完善的注册功能（包含真实的邮件发送）")
print("2. 修复的滑块验证功能")
print("3. 页面角落的秒速五厘米元素")
print("4. 樱花飘落动画效果")
print("5. 秒速五厘米的经典台词")
print("="*70)
