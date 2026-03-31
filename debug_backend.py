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
print("调试后端代码")
print("="*60)

# 1. 杀死所有node进程
print("\n=== 1. 清理所有node进程 ===")
run_command(ssh, "pkill -9 -f 'tsx|node' 2>&1 || true")
run_command(ssh, "sleep 1")

# 2. 检查端口占用
print("\n=== 2. 检查端口占用 ===")
out, err = run_command(ssh, "ss -tlnp | grep 3001")
print(out)

# 3. 创建一个简单的测试服务器
print("\n=== 3. 创建测试服务器 ===")
test_server = """
const express = require('express');
const app = express();
const PORT = 3001;

app.get('/api/health', (req, res) => {
  res.json({ success: true, message: '测试服务器运行正常' });
});

app.get('/api/animes', (req, res) => {
  res.json({
    success: true,
    data: [
      { id: 1, title: '测试动漫1' },
      { id: 2, title: '测试动漫2' }
    ]
  });
});

app.listen(PORT, () => {
  console.log(`测试服务器运行在端口 ${PORT}`);
});
"""
run_command(ssh, f"cat > /opt/anime-website/backend/test-server.js <<'EOF'\n{test_server}\nEOF")

# 4. 运行测试服务器
print("\n=== 4. 运行测试服务器 ===")
run_command(ssh, "cd /opt/anime-website/backend && node test-server.js 2>&1 &")
run_command(ssh, "sleep 2")

# 5. 测试API
print("\n=== 5. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print(out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes 2>&1")
print(out)

# 6. 停止测试服务器
run_command(ssh, "pkill -9 -f 'node test-server.js' 2>&1 || true")

# 7. 检查原后端代码问题
print("\n=== 7. 检查原后端代码问题 ===")
out, err = run_command(ssh, "cd /opt/anime-website/backend && npx tsx server-simple.ts 2>&1 &")
run_command(ssh, "sleep 3")
out, err = run_command(ssh, "ps aux | grep tsx | grep -v grep | head -3")
print(out)

run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1 || true")

ssh.close()
