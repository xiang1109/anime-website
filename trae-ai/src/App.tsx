import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import type { Anime } from './types';
import Navbar from './components/Navbar';
import AnimeCard from './components/AnimeCard';
import LoginModal from './components/LoginModal';
import RegisterModal from './components/RegisterModal';
import AnimeDetailModal from './components/AnimeDetailModal';
import SearchPage from './pages/SearchPage';
import AdminPage from './pages/AdminPage';
import YourNameCorner from './components/YourNameCorner';
import { useAuth } from './context/AuthContext';
import API_BASE_URL from './config/api';

// 樱花飘落效果组件
const SakuraFall: React.FC = () => {
  useEffect(() => {
    const createPetal = () => {
      const petal = document.createElement('div');
      petal.className = 'sakura-petal';
      
      // 随机大小
      const size = Math.random() * 10 + 5;
      petal.style.width = `${size}px`;
      petal.style.height = `${size}px`;
      
      // 随机位置
      petal.style.left = `${Math.random() * 100}vw`;
      petal.style.top = '-20px';
      
      // 随机动画持续时间
      const duration = Math.random() * 10 + 10;
      petal.style.animationDuration = `${duration}s`;
      
      // 随机延迟
      petal.style.animationDelay = `${Math.random() * 5}s`;
      
      // 随机动画方向
      petal.style.transform = `rotate(${Math.random() * 360}deg)`;
      
      document.body.appendChild(petal);
      
      // 动画结束后移除元素
      setTimeout(() => {
        if (petal.parentNode) {
          petal.parentNode.removeChild(petal);
        }
      }, duration * 1000);
    };
    
    // 初始创建樱花
    for (let i = 0; i < 20; i++) {
      setTimeout(createPetal, i * 500);
    }
    
    // 持续创建樱花
    const interval = setInterval(createPetal, 2000);
    
    return () => clearInterval(interval);
  }, []);
  
  return null;
};

// 首页组件
const HomePage: React.FC = () => {
  const [animeList, setAnimeList] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [selectedAnime, setSelectedAnime] = useState<Anime | null>(null);
  const [showAnimeDetail, setShowAnimeDetail] = useState(false);
  const [currentAnimePage, setCurrentAnimePage] = useState(1);
  const [totalAnimePages, setTotalAnimePages] = useState(1);
  const { user, isLoading: authLoading } = useAuth();

  useEffect(() => {
    fetchAnimeList(currentAnimePage);
  }, [currentAnimePage]);

  const fetchAnimeList = async (page: number = 1) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/anime?page=${page}&limit=12`);
      const result = await response.json();
      const data = result.data || result;
      setAnimeList(data.animes || data);
      setTotalAnimePages(data.pagination?.totalPages || 1);
    } catch (error) {
      console.error('Failed to fetch anime list:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnimeClick = (anime: Anime) => {
    setSelectedAnime(anime);
    setShowAnimeDetail(true);
  };

  const handlePageChange = (page: number) => {
    setCurrentAnimePage(page);
  };

  // 生成分页页码（优化显示）
  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;
    
    if (totalAnimePages <= maxVisible) {
      for (let i = 1; i <= totalAnimePages; i++) {
        pages.push(i);
      }
    } else {
      if (currentAnimePage <= 3) {
        for (let i = 1; i <= maxVisible; i++) {
          pages.push(i);
        }
      } else if (currentAnimePage >= totalAnimePages - 2) {
        for (let i = totalAnimePages - maxVisible + 1; i <= totalAnimePages; i++) {
          pages.push(i);
        }
      } else {
        for (let i = currentAnimePage - 2; i <= currentAnimePage + 2; i++) {
          pages.push(i);
        }
      }
    }
    
    return pages;
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-text">加载中...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar
        onLoginClick={() => setShowLogin(true)}
        onRegisterClick={() => setShowRegister(true)}
        onSearchClick={() => {}}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-text mb-2">高分动漫</h1>
          <p className="text-text-muted">发现最受欢迎的动漫作品，为你喜爱的作品打分</p>
        </div>

        {/* 快捷搜索入口 */}
        <div className="bg-surface border border-border rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h3 className="text-lg font-semibold text-text mb-1">寻找特定动漫？</h3>
              <p className="text-sm text-text-muted">使用搜索功能快速找到你想看的动漫</p>
            </div>
            <a
              href="/search"
              className="btn-primary px-6 py-2 text-white rounded-lg font-medium flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              开始搜索
            </a>
          </div>
        </div>

        {user && (
          <div className="bg-surface border border-border rounded-xl p-4 mb-8">
            <p className="text-text">
              欢迎回来，<span className="font-semibold text-primary">{user.username}</span>！
              去探索精彩的动漫世界吧！
            </p>
          </div>
        )}

        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-text-muted">加载中...</div>
          </div>
        ) : animeList.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-text-muted mb-4">暂无动漫数据</div>
            <p className="text-sm text-text-muted">请确保后端服务已启动并连接到数据库</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {animeList.map((anime) => (
                <AnimeCard
                  key={anime.id}
                  anime={anime}
                  onClick={() => handleAnimeClick(anime)}
                />
              ))}
            </div>

            {/* 分页 */}
            {totalAnimePages > 1 && (
              <div className="flex items-center justify-center gap-2">
                <button
                  onClick={() => handlePageChange(currentAnimePage - 1)}
                  disabled={currentAnimePage === 1}
                  className="px-4 py-2 bg-surface border border-border rounded-lg text-text disabled:opacity-50 disabled:cursor-not-allowed hover:border-primary/50 transition-colors"
                >
                  上一页
                </button>
                
                <div className="flex items-center gap-1">
                  {getPageNumbers().map((page) => (
                    <button
                      key={page}
                      onClick={() => handlePageChange(page)}
                      className={`w-10 h-10 rounded-lg text-sm font-medium transition-colors ${
                        page === currentAnimePage
                          ? 'bg-primary text-white'
                          : 'bg-surface border border-border text-text hover:border-primary/50'
                      }`}
                    >
                      {page}
                    </button>
                  ))}
                </div>

                <button
                  onClick={() => handlePageChange(currentAnimePage + 1)}
                  disabled={currentAnimePage === totalAnimePages}
                  className="px-4 py-2 bg-surface border border-border rounded-lg text-text disabled:opacity-50 disabled:cursor-not-allowed hover:border-primary/50 transition-colors"
                >
                  下一页
                </button>
              </div>
            )}
          </>
        )}
      </main>

      <footer className="bg-surface border-t border-border mt-12 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-text-muted text-sm">
            © 2024 动漫评分 - 发现精彩的动漫世界
          </p>
        </div>
      </footer>

      <LoginModal
        isOpen={showLogin}
        onClose={() => setShowLogin(false)}
        onSwitchToRegister={() => {
          setShowLogin(false);
          setShowRegister(true);
        }}
      />

      <RegisterModal
        isOpen={showRegister}
        onClose={() => setShowRegister(false)}
        onSwitchToLogin={() => {
          setShowRegister(false);
          setShowLogin(true);
        }}
      />

      <AnimeDetailModal
        isOpen={showAnimeDetail}
        onClose={() => setShowAnimeDetail(false)}
        anime={selectedAnime}
      />
    </div>
  );
};

// 搜索页面组件
const SearchPageWrapper: React.FC = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      <Navbar
        onLoginClick={() => setShowLogin(true)}
        onRegisterClick={() => setShowRegister(true)}
        showHome={true}
        onHomeClick={() => navigate('/')}
      />
      <SearchPage />
      
      <LoginModal
        isOpen={showLogin}
        onClose={() => setShowLogin(false)}
        onSwitchToRegister={() => {
          setShowLogin(false);
          setShowRegister(true);
        }}
      />

      <RegisterModal
        isOpen={showRegister}
        onClose={() => setShowRegister(false)}
        onSwitchToLogin={() => {
          setShowRegister(false);
          setShowLogin(true);
        }}
      />
    </div>
  );
};

// 管理员路由保护组件
const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isAdmin, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-text">加载中...</div>
      </div>
    );
  }

  if (!user || !isAdmin) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};

function App() {
  return (
    <BrowserRouter>
      <YourNameCorner />
      <SakuraFall />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPageWrapper />} />
        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminPage />
            </AdminRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
