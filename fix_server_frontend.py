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

print("="*60)
print("修复服务器上的前端问题")
print("="*60)

# 1. 检查服务器状态
print("\n=== 1. 检查服务器状态 ===")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print("后端状态:", out.strip())

out, err = run_command(ssh, "systemctl is-active nginx")
print("Nginx状态:", out.strip())

out, err = run_command(ssh, "systemctl is-active mysqld")
print("MySQL状态:", out.strip())

# 2. 测试API
print("\n=== 2. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/anime?page=1&limit=1 2>&1")
print("后端API:", out[:100])

out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1 2>&1")
print("Nginx API:", out[:100])

# 3. 检查前端文件
print("\n=== 3. 检查前端文件 ===")
out, err = run_command(ssh, "ls -la /usr/share/nginx/html/")
print(out)

# 4. 创建一个简单的测试页面
print("\n=== 4. 创建测试页面 ===")
test_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>动漫网站 - 测试</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold mb-8">🎬 动漫网站</h1>
        
        <div class="bg-gray-800 rounded-lg p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">服务器状态</h2>
            <div id="status" class="space-y-2">
                <p>正在检查...</p>
            </div>
        </div>

        <div class="bg-gray-800 rounded-lg p-6">
            <h2 class="text-2xl font-bold mb-4">动漫列表</h2>
            <div id="anime-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <p>正在加载...</p>
            </div>
        </div>
    </div>

    <script>
        async function checkStatus() {
            const statusDiv = document.getElementById('status');
            
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                statusDiv.innerHTML = `
                    <p class="text-green-400">✅ API状态: ${data.message}</p>
                `;
            } catch (error) {
                statusDiv.innerHTML = `<p class="text-red-400">❌ API状态: 连接失败</p>`;
            }
        }

        async function loadAnime() {
            const animeList = document.getElementById('anime-list');
            
            try {
                const response = await fetch('/api/anime?page=1&limit=8');
                const result = await response.json();
                
                if (result.success && result.data && result.data.animes) {
                    const animes = result.data.animes;
                    animeList.innerHTML = animes.map(anime => `
                        <div class="bg-gray-700 rounded-lg overflow-hidden">
                            <img src="${anime.cover_image || 'https://picsum.photos/300/400'}" 
                                 alt="${anime.title}" 
                                 class="w-full h-64 object-cover">
                            <div class="p-4">
                                <h3 class="font-bold text-lg mb-1">${anime.title}</h3>
                                <p class="text-sm text-gray-400 mb-2">${anime.studio || ''}</p>
                                <div class="flex items-center gap-2">
                                    <span class="text-yellow-400">⭐ ${anime.average_rating || 'N/A'}</span>
                                    <span class="text-gray-400">${anime.episodes || '?'} 集</span>
                                </div>
                            </div>
                        </div>
                    `).join('');
                } else {
                    animeList.innerHTML = '<p class="text-red-400">暂无动漫数据</p>';
                }
            } catch (error) {
                animeList.innerHTML = `<p class="text-red-400">加载失败: ${error.message}</p>`;
            }
        }

        checkStatus();
        loadAnime();
    </script>
</body>
</html>
"""
run_command(ssh, f"cat > /usr/share/nginx/html/test.html <<'EOF'\n{test_html}\nEOF")
print("测试页面已创建")

# 5. 访问测试页面
print("\n=== 5. 测试页面访问 ===")
out, err = run_command(ssh, "curl -s http://localhost/test.html | head -20")
print(out[:500])

ssh.close()

print("\n" + "="*60)
print("修复完成！")
print("="*60)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n或者访问测试页面：")
print("http://59.110.214.50/test.html")
print("="*60)
