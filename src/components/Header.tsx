import { useState, useRef, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import SearchBar from './SearchBar';
import LoginModal from './LoginModal';
import RegisterModal from './RegisterModal';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const userMenuRef = useRef<HTMLDivElement>(null);

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/', label: '首页', labelEn: 'Home', icon: '🏠' },
    { path: '/daily', label: '每日推荐', labelEn: 'Daily', icon: '⭐' },
    { path: '/hidden-gems', label: '冷门佳作', labelEn: 'Hidden Gems', icon: '💎' },
    { path: '/ongoing', label: '连载动漫', labelEn: 'Ongoing', icon: '📺' },
    { path: '/completed', label: '完结动漫', labelEn: 'Completed', icon: '✅' },
    { path: '/theater', label: '剧场版', labelEn: 'Theater', icon: '🎬' },
  ];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setShowUserMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSearchComplete = () => {
    setShowSearch(false);
    navigate('/search');
  };

  const switchToRegister = () => {
    setShowLoginModal(false);
    setShowRegisterModal(true);
  };

  const switchToLogin = () => {
    setShowRegisterModal(false);
    setShowLoginModal(true);
  };

  return (
    <>
      <header className="sticky top-0 z-50 bg-surface/80 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo */}
            <Link to="/" className="flex-shrink-0 group">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="w-10 h-10 bg-gradient-to-br from-pink-500 via-purple-500 to-cyan-500 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/30 group-hover:shadow-purple-500/50 transition-all group-hover:scale-110">
                    <span className="text-white font-bold text-lg">漫</span>
                  </div>
                  <div className="absolute -inset-1 bg-gradient-to-br from-pink-500 via-purple-500 to-cyan-500 rounded-xl blur-md opacity-50 group-hover:opacity-75 transition-opacity" />
                </div>
                <div>
                  <span className="text-xl font-bold text-white group-hover:rainbow-text transition-all">雾漫林间</span>
                  <span className="block text-xs text-white/50 -mt-1">Anime World</span>
                </div>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-1">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`relative px-4 py-2 rounded-xl text-sm font-medium transition-all group ${
                    isActive(item.path) 
                      ? 'text-white' 
                      : 'text-white/60 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <span className="mr-1.5">{item.icon}</span>
                  {item.label}
                  {isActive(item.path) && (
                    <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-1 h-1 bg-gradient-to-r from-pink-500 to-cyan-500 rounded-full" />
                  )}
                </Link>
              ))}
            </nav>

            {/* Right Section */}
            <div className="flex items-center gap-3">
              {/* Search Button - Desktop */}
              <button
                onClick={() => setShowSearch(!showSearch)}
                className="hidden sm:flex items-center justify-center w-11 h-11 rounded-xl bg-white/5 hover:bg-white/10 text-white/70 hover:text-white transition-all hover:scale-105"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>

              {/* User Menu */}
              {user ? (
                <div className="relative" ref={userMenuRef}>
                  <button
                    onClick={() => setShowUserMenu(!showUserMenu)}
                    className="flex items-center gap-2 rounded-xl bg-white/5 hover:bg-white/10 p-1.5 pr-3 transition-all hover:scale-105"
                  >
                    {user.avatar ? (
                      <img
                        src={user.avatar} alt={user.username} className="w-9 h-9 rounded-lg object-cover ring-2 ring-white/20" />
                      ) : (
                        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-pink-500 to-purple-500 flex items-center justify-center ring-2 ring-white/20">
                          <span className="text-white text-sm">👤</span>
                        </div>
                      )}
                    <span className="text-white font-medium text-sm">{user.username}</span>
                    <svg className={`w-4 h-4 text-white/50 transition-transform ${showUserMenu ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {/* Dropdown Menu */}
                  {showUserMenu && (
                    <div className="absolute right-0 mt-3 w-64 bg-surface border border-white/10 rounded-2xl shadow-2xl py-2 z-50 glass overflow-hidden">
                      <div className="px-4 py-3 border-b border-white/10 bg-gradient-to-r from-pink-500/10 to-purple-500/10">
                        <p className="text-sm font-semibold text-white flex items-center gap-2">
                          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                          {user.username}
                        </p>
                        {user.email && (
                          <p className="text-xs text-white/60 mt-1 truncate">{user.email}</p>
                        )}
                      </div>
                      <Link
                        to="/profile"
                        onClick={() => setShowUserMenu(false)}
                        className="flex items-center gap-3 px-4 py-2.5 text-sm text-white hover:bg-white/5 transition-colors mx-2 rounded-lg"
                      >
                        <span className="w-8 h-8 bg-pink-500/20 rounded-lg flex items-center justify-center">👤</span>
                        <span>个人中心</span>
                      </Link>
                      {user?.username === 'admin' && (
                        <>
                          <Link
                            to="/admin"
                            onClick={() => setShowUserMenu(false)}
                            className="flex items-center gap-3 px-4 py-2.5 text-sm text-white hover:bg-white/5 transition-colors mx-2 rounded-lg"
                          >
                            <span className="w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center">⚙️</span>
                            <span>管理后台</span>
                          </Link>
                          <Link
                            to="/anime-manager"
                            onClick={() => setShowUserMenu(false)}
                            className="flex items-center gap-3 px-4 py-2.5 text-sm text-white hover:bg-white/5 transition-colors mx-2 rounded-lg"
                          >
                            <span className="w-8 h-8 bg-cyan-500/20 rounded-lg flex items-center justify-center">🎬</span>
                            <span>动漫图片管理</span>
                          </Link>
                        </>
                      )}
                      <div className="border-t border-white/10 my-2 mx-4" />
                      <button
                        onClick={() => {
                          setShowUserMenu(false);
                          logout();
                        }}
                        className="flex items-center gap-3 px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 transition-colors w-full mx-2 rounded-lg"
                      >
                        <span className="w-8 h-8 bg-red-500/20 rounded-lg flex items-center justify-center">🚪</span>
                        <span>退出登录</span>
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setShowLoginModal(true)}
                    className="hidden sm:flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-white hover:text-white/80 transition-colors"
                  >
                    登录
                  </button>
                  <button
                    onClick={() => setShowRegisterModal(true)}
                    className="flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-pink-500 to-purple-500 rounded-xl hover:from-pink-600 hover:to-purple-600 shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 transition-all hover:scale-105"
                  >
                    <span>✨</span>
                    注册
                  </button>
                </div>
              )}

              {/* Mobile Menu Button */}
              <button
                className="md:hidden p-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-white"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
              >
                {isMenuOpen ? (
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                ) : (
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        {showSearch && (
          <div className="border-t border-white/10 bg-surface/95 backdrop-blur-xl">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
              <SearchBar onSearch={handleSearchComplete} />
            </div>
          </div>
        )}

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-white/10 bg-surface/95 backdrop-blur-xl">
            <div className="px-4 py-4 space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsMenuOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl text-base font-medium transition-all ${
                    isActive(item.path)
                      ? 'bg-gradient-to-r from-pink-500/20 to-purple-500/20 text-white border border-pink-500/30'
                      : 'text-white/70 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <span className="text-xl">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        )}
      </header>

      <LoginModal 
        isOpen={showLoginModal} 
        onClose={() => setShowLoginModal(false)}
        onSwitchToRegister={switchToRegister}
      />
      
      <RegisterModal 
        isOpen={showRegisterModal} 
        onClose={() => setShowRegisterModal(false)}
        onSwitchToLogin={switchToLogin}
      />
    </>
  );
};

export default Header;
