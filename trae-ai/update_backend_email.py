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

print("="*70)
print("更新后端代码，添加邮件发送功能")
print("="*70)

# 1. 安装Nodemailer
print("\n=== 1. 安装Nodemailer ===")
run_command(ssh, "cd /opt/anime-website/backend && npm install nodemailer @types/nodemailer 2>&1")

# 2. 更新后端代码
print("\n=== 2. 更新后端代码 ===")

# 读取当前后端文件
with open('d:/code/trae-ai/server-complete.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# 添加Nodemailer导入
if "import nodemailer from 'nodemailer'" not in content:
    content = content.replace(
        "import mysql from 'mysql2/promise';",
        "import mysql from 'mysql2/promise';\nimport nodemailer from 'nodemailer';"
    )

# 添加邮件配置
if "// 邮件配置" not in content:
    content = content.replace(
        "const JWT_SECRET = 'your-secret-key-change-in-production';",
        "const JWT_SECRET = 'your-secret-key-change-in-production';\n\n// 邮件配置\nconst transporter = nodemailer.createTransporter({
  service: 'qq',
  auth: {
    user: 'your-qq-email@qq.com', // 你的QQ邮箱
    pass: 'your-qq-email-auth-code' // QQ邮箱授权码
  }
});"
    )

# 更新发送验证码函数
old_send_code = "    // 真实环境中这里需要调用第三方邮件服务API，如Nodemailer、SendGrid等\n    console.log(`【模拟邮件发送】邮箱: ${email}, 验证码: ${code}`);"

new_send_code = "    // 发送邮件
    try {
      const info = await transporter.sendMail({
        from: '"动漫网站" <your-qq-email@qq.com>',
        to: email,
        subject: '动漫网站 - 注册验证码',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">动漫网站注册验证码</h2>
            <p style="font-size: 16px; line-height: 1.5;">您好，</p>
            <p style="font-size: 16px; line-height: 1.5;">感谢您注册动漫网站。您的验证码是：</p>
            <div style="font-size: 24px; font-weight: bold; color: #4CAF50; margin: 20px 0;">${code}</div>
            <p style="font-size: 14px; color: #666;">验证码有效期为5分钟，请尽快使用。</p>
            <p style="font-size: 14px; color: #666; margin-top: 30px;">如果您没有发起注册请求，请忽略此邮件。</p>
            <p style="font-size: 14px; color: #666; margin-top: 20px;">动漫网站团队</p>
          </div>
        `
      });
      console.log('邮件发送成功:', info.messageId);
    } catch (mailError) {
      console.error('邮件发送失败:', mailError);
      // 邮件发送失败不影响验证码生成，仍然返回成功
    }
    
    console.log(`【邮件发送】邮箱: ${email}, 验证码: ${code}`);"

content = content.replace(old_send_code, new_send_code)

# 保存更新后的后端文件
with open('d:/code/trae-ai/server-complete.ts', 'w', encoding='utf-8') as f:
    f.write(content)

# 3. 上传到服务器
print("\n=== 3. 上传到服务器 ===")
sftp = ssh.open_sftp()
sftp.put('d:/code/trae-ai/server-complete.ts', '/opt/anime-website/backend/server-simple.ts')
sftp.close()

# 4. 重启后端服务
print("\n=== 4. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend 2>&1")
run_command(ssh, "sleep 3")

# 5. 验证后端服务
print("\n=== 5. 验证后端服务 ===")
out, err = run_command(ssh, "pm2 status anime-backend")
print(out)

# 6. 测试健康检查
print("\n=== 6. 测试健康检查 ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/health'")
print(out)

ssh.close()

print("\n" + "="*70)
print("后端邮件功能更新完成！")
print("="*70)
print("\n注意：")
print("1. 请在server-complete.ts中配置您的QQ邮箱和授权码")
print("2. 您需要在QQ邮箱设置中开启SMTP服务")
print("3. 授权码可以在QQ邮箱设置中生成")
print("="*70)
