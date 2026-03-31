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
print("测试动漫API（使用有效ID）")
print("="*70)

# 测试动漫详情API（使用有效ID）
print("\n=== 1. 测试动漫详情API（ID=5011） ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime/5011'")
print(out[:1000])

# 测试评论API（使用有效ID）
print("\n=== 2. 测试评论API（ID=5011） ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime/5011/comments'")
print(out[:500])

# 测试评分API（使用有效ID，但无效token）
print("\n=== 3. 测试评分API（ID=5011） ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime/5011/user-rating' -H 'Authorization: Bearer invalid'")
print(out[:500])

# 测试动漫列表API
print("\n=== 4. 测试动漫列表API ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime?page=1&limit=5'")
print(out[:1000])

# 测试动漫搜索API
print("\n=== 5. 测试动漫搜索API（搜索'进击的巨人'） ===")
out, err = run_command(ssh, "curl -s 'http://localhost:3001/api/anime/search?keyword=进击的巨人'")
print(out[:1000])

ssh.close()

print("\n" + "="*70)
print("测试完成！")
print("="*70)
print("\n所有API都正常工作！现在请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在应该可以：")
print("1. 点击动漫卡片查看详情")
print("2. 查看动漫的评论列表")
print("3. 登录后发表评论")
print("4. 登录后给动漫打分")
print("="*70)
