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
print("创建完整的前端页面")
print("="*70)

# 创建完整的HTML页面
complete_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>动漫网站</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .anime-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        .anime-card {
            transition: all 0.3s ease;
        }
        .loading {
            display: inline-block;
            width: 30px;
            height: 30px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <!-- 导航栏 -->
    <nav class="bg-gray-800 shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4">
            <div class="flex items-center justify-between">
                <h1 class="text-2xl font-bold text-yellow-400">🎬 动漫网站</h1>
                <div class="flex items-center gap-4">
                    <button id="loginBtn" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition">登录</button>
                    <button id="registerBtn" class="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition">注册</button>
                </div>
            </div>
        </div>
    </nav>

    <!-- 主要内容 -->
    <main class="max-w-7xl mx-auto px-4 py-8">
        <!-- 搜索栏 -->
        <div class="mb-8">
            <div class="flex gap-4">
                <input 
                    type="text" 
                    id="searchInput" 
                    placeholder="搜索动漫..." 
                    class="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-yellow-400 transition"
                >
                <button id="searchBtn" class="bg-yellow-500 hover:bg-yellow-600 text-black font-bold px-6 py-3 rounded-lg transition">
                    搜索
                </button>
            </div>
        </div>

        <!-- 状态信息 -->
        <div id="statusInfo" class="mb-6 p-4 bg-gray-800 rounded-lg hidden">
            <p id="statusText"></p>
        </div>

        <!-- 加载状态 -->
        <div id="loading" class="text-center py-20">
            <div class="loading"></div>
            <p class="mt-4 text-gray-400">正在加载动漫数据...</p>
        </div>

        <!-- 动漫列表 -->
        <div id="animeList" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 hidden">
        </div>

        <!-- 分页 -->
        <div id="pagination" class="mt-8 flex justify-center gap-2 hidden">
        </div>

        <!-- 空状态 -->
        <div id="emptyState" class="text-center py-20 hidden">
            <p class="text-gray-400 text-xl">暂无动漫数据</p>
        </div>
    </main>

    <!-- 登录模态框 -->
    <div id="loginModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4">
            <h2 class="text-2xl font-bold mb-6">登录</h2>
            <form id="loginForm">
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">用户名</label>
                    <input type="text" id="loginUsername" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-yellow-400">
                </div>
                <div class="mb-6">
                    <label class="block text-gray-400 mb-2">密码</label>
                    <input type="password" id="loginPassword" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-yellow-400">
                </div>
                <div class="flex gap-4">
                    <button type="submit" class="flex-1 bg-blue-600 hover:bg-blue-700 py-2 rounded-lg transition">登录</button>
                    <button type="button" id="closeLoginModal" class="flex-1 bg-gray-600 hover:bg-gray-700 py-2 rounded-lg transition">取消</button>
                </div>
            </form>
        </div>
    </div>

    <!-- 注册模态框 -->
    <div id="registerModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4">
            <h2 class="text-2xl font-bold mb-6">注册</h2>
            <form id="registerForm">
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">用户名</label>
                    <input type="text" id="registerUsername" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-yellow-400">
                </div>
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">邮箱</label>
                    <input type="email" id="registerEmail" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-yellow-400">
                </div>
                <div class="mb-6">
                    <label class="block text-gray-400 mb-2">密码</label>
                    <input type="password" id="registerPassword" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-yellow-400">
                </div>
                <div class="flex gap-4">
                    <button type="submit" class="flex-1 bg-green-600 hover:bg-green-700 py-2 rounded-lg transition">注册</button>
                    <button type="button" id="closeRegisterModal" class="flex-1 bg-gray-600 hover:bg-gray-700 py-2 rounded-lg transition">取消</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        let currentPage = 1;
        const limit = 12;
        let totalPages = 1;

        const loading = document.getElementById('loading');
        const animeList = document.getElementById('animeList');
        const pagination = document.getElementById('pagination');
        const emptyState = document.getElementById('emptyState');
        const statusInfo = document.getElementById('statusInfo');
        const statusText = document.getElementById('statusText');

        const loginModal = document.getElementById('loginModal');
        const registerModal = document.getElementById('registerModal');

        function showStatus(message, isError = false) {
            statusInfo.classList.remove('hidden');
            statusText.textContent = message;
            statusText.className = isError ? 'text-red-400' : 'text-green-400';
            setTimeout(() => {
                statusInfo.classList.add('hidden');
            }, 3000);
        }

        async function loadAnime(page = 1, search = '') {
            loading.classList.remove('hidden');
            animeList.classList.add('hidden');
            pagination.classList.add('hidden');
            emptyState.classList.add('hidden');

            try {
                console.log('正在加载动漫数据...');
                let url = `/api/anime?page=${page}&limit=${limit}`;
                if (search) {
                    url += `&search=${encodeURIComponent(search)}`;
                }

                const response = await fetch(url);
                console.log('响应状态:', response.status);

                if (!response.ok) {
                    throw new Error(`HTTP错误: ${response.status}`);
                }

                const result = await response.json();
                console.log('响应数据:', result);

                if (result.success && result.data && result.data.animes) {
                    const animes = result.data.animes;
                    const paginationData = result.data.pagination;

                    if (animes.length === 0) {
                        emptyState.classList.remove('hidden');
                    } else {
                        currentPage = paginationData.page;
                        totalPages = paginationData.totalPages;

                        renderAnimeList(animes);
                        renderPagination();
                        animeList.classList.remove('hidden');
                        pagination.classList.remove('hidden');
                    }
                } else {
                    throw new Error('数据格式错误');
                }
            } catch (error) {
                console.error('加载失败:', error);
                showStatus(`加载失败: ${error.message}`, true);
                emptyState.classList.remove('hidden');
            } finally {
                loading.classList.add('hidden');
            }
        }

        function renderAnimeList(animes) {
            animeList.innerHTML = animes.map(anime => `
                <div class="anime-card bg-gray-800 rounded-lg overflow-hidden cursor-pointer" data-id="${anime.id}">
                    <img 
                        src="${anime.cover_image || 'https://picsum.photos/300/400'}" 
                        alt="${anime.title}" 
                        class="w-full h-64 object-cover"
                        onerror="this.src='https://picsum.photos/300/400?random=${anime.id}'"
                    >
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

            document.querySelectorAll('.anime-card').forEach(card => {
                card.addEventListener('click', () => {
                    const id = card.dataset.id;
                    alert(`点击了动漫 ID: ${id}`);
                });
            });
        }

        function renderPagination() {
            let paginationHTML = '';

            if (currentPage > 1) {
                paginationHTML += `<button class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition" onclick="loadAnime(${currentPage - 1})">上一页</button>`;
            }

            paginationHTML += `<span class="px-4 py-2 bg-gray-800 rounded-lg">${currentPage} / ${totalPages}</span>`;

            if (currentPage < totalPages) {
                paginationHTML += `<button class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition" onclick="loadAnime(${currentPage + 1})">下一页</button>`;
            }

            pagination.innerHTML = paginationHTML;
        }

        document.getElementById('searchBtn').addEventListener('click', () => {
            const search = document.getElementById('searchInput').value;
            loadAnime(1, search);
        });

        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const search = document.getElementById('searchInput').value;
                loadAnime(1, search);
            }
        });

        document.getElementById('loginBtn').addEventListener('click', () => {
            loginModal.classList.remove('hidden');
        });

        document.getElementById('closeLoginModal').addEventListener('click', () => {
            loginModal.classList.add('hidden');
        });

        document.getElementById('registerBtn').addEventListener('click', () => {
            registerModal.classList.remove('hidden');
        });

        document.getElementById('closeRegisterModal').addEventListener('click', () => {
            registerModal.classList.add('hidden');
        });

        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                const result = await response.json();
                if (result.success) {
                    showStatus('登录成功！');
                    loginModal.classList.add('hidden');
                } else {
                    showStatus(result.message || '登录失败', true);
                }
            } catch (error) {
                showStatus('登录失败: ' + error.message, true);
            }
        });

        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('registerUsername').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;

            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, email, password })
                });

                const result = await response.json();
                if (result.success) {
                    showStatus('注册成功！');
                    registerModal.classList.add('hidden');
                } else {
                    showStatus(result.message || '注册失败', true);
                }
            } catch (error) {
                showStatus('注册失败: ' + error.message, true);
            }
        });

        loginModal.addEventListener('click', (e) => {
            if (e.target === loginModal) {
                loginModal.classList.add('hidden');
            }
        });

        registerModal.addEventListener('click', (e) => {
            if (e.target === registerModal) {
                registerModal.classList.add('hidden');
            }
        });

        loadAnime();
    </script>
</body>
</html>
"""

# 写入HTML文件
print("\n=== 1. 写入HTML文件 ===")
run_command(ssh, f"cat > /usr/share/nginx/html/index.html <<'EOF'\n{complete_html}\nEOF")
print("HTML文件已写入")

# 设置权限
print("\n=== 2. 设置文件权限 ===")
run_command(ssh, "chown -R nginx:nginx /usr/share/nginx/html/")
print("权限已设置")

# 测试页面访问
print("\n=== 3. 测试页面访问 ===")
out, err = run_command(ssh, "curl -s -o /dev/null -w '%{http_code}' http://localhost 2>&1")
print("HTTP状态码:", out.strip())

# 测试API
print("\n=== 4. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=1")
print("API响应:", out[:100])

ssh.close()

print("\n" + "="*70)
print("完整前端页面创建完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在应该能看到：")
print("1. 动漫列表显示")
print("2. 搜索功能")
print("3. 分页功能")
print("4. 登录/注册按钮")
print("="*70)
