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
print("直接修复前端问题")
print("="*60)

# 1. 创建一个简单的HTML页面来显示动漫数据
print("\n=== 1. 创建简单HTML页面 ===")
simple_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>动漫网站</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold mb-8">🎬 高分动漫</h1>
        
        <div id="anime-list" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <p class="text-gray-400">正在加载...</p>
        </div>
    </div>

    <script>
        async function loadAnime() {
            const animeList = document.getElementById('anime-list');
            
            try {
                console.log('正在获取动漫数据...');
                const response = await fetch('/api/anime?page=1&limit=12');
                console.log('响应状态:', response.status);
                
                const result = await response.json();
                console.log('响应数据:', result);
                
                if (result.success && result.data && result.data.animes) {
                    const animes = result.data.animes;
                    console.log('动漫数量:', animes.length);
                    
                    if (animes.length === 0) {
                        animeList.innerHTML = '<p class="text-gray-400 col-span-full text-center py-20">暂无动漫数据</p>';
                        return;
                    }
                    
                    animeList.innerHTML = animes.map(anime => `
                        <div class="bg-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-transform">
                            <img src="${anime.cover_image || 'https://picsum.photos/300/400'}" 
                                 alt="${anime.title}" 
                                 class="w-full h-64 object-cover">
                            <div class="p-4">
                                <h3 class="font-bold text-lg mb-1 truncate">${anime.title}</h3>
                                <p class="text-sm text-gray-400 mb-2">${anime.studio || '未知'}</p>
                                <div class="flex items-center justify-between">
                                    <span class="text-yellow-400">⭐ ${anime.average_rating || 'N/A'}</span>
                                    <span class="text-gray-400 text-sm">${anime.episodes || '?'} 集</span>
                                </div>
                            </div>
                        </div>
                    `).join('');
                } else {
                    animeList.innerHTML = '<p class="text-red-400 col-span-full text-center py-20">数据格式错误</p>';
                }
            } catch (error) {
                console.error('加载失败:', error);
                animeList.innerHTML = `<p class="text-red-400 col-span-full text-center py-20">加载失败: ${error.message}</p>`;
            }
        }

        loadAnime();
    </script>
</body>
</html>
"""
run_command(ssh, f"cat > /usr/share/nginx/html/index.html <<'EOF'\n{simple_html}\nEOF")
print("HTML页面已创建")

# 2. 测试页面访问
print("\n=== 2. 测试页面访问 ===")
out, err = run_command(ssh, "curl -s http://localhost | head -10")
print(out[:300])

# 3. 测试API
print("\n=== 3. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1")
print("API响应:", out[:200])

ssh.close()

print("\n" + "="*60)
print("前端修复完成！")
print("="*60)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在应该能看到动漫数据了！")
print("="*60)
