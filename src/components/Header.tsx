import { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { UserCircle, Search, Menu, X, LogIn, User, Settings, LogOut, ChevronDown } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import SearchBar from './SearchBar';

const Header: React.FC = () => {
  const { user, logout, isAdmin } = useAuth();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const userMenuRef = useRef<HTMLDivElement>(null);

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/', label: '首页', labelEn: 'Home' },
    { path: '/daily', label: '每日推荐', labelEn: 'Daily' },
    { path: '/hidden-gems', label: '冷门佳作', labelEn: 'Hidden Gems' },
    { path: '/ongoing', label: '连载动漫', labelEn: 'Ongoing' },
    { path: '/completed', label: '完结动漫', labelEn: 'Completed' },
    { path: '/chinese', label: '国产动漫', labelEn: 'Chinese' },
    { path: '/japanese', label: '日本动漫', labelEn: 'Japanese' },
    { path: '/theater', label: '剧场版', labelEn: 'Theater' },
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

  return (
    <header className="bg-surface border-b border-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex-shrink-0">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">漫</span>
              </div>
              <span className="text-xl font-bold text-text">雾漫林间</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`text-sm font-medium transition-colors hover:text-primary ${
                  isActive(item.path) ? 'text-primary' : 'text-text-muted'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Right Section */}
          <div className="flex items-center gap-4">
            {/* Search Button - Desktop */}
            <button
              onClick={() => setShowSearch(!showSearch)}
              className="hidden sm:flex items-center justify-center w-10 h-10 rounded-full hover:bg-background transition-colors"
            >
              <Search className="w-5 h-5 text-text-muted" />
            </button>

            {/* User Menu */}
            {user ? (
              <div className="relative" ref={userMenuRef}>
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 rounded-full hover:bg-background p-1 transition-colors"
                >
                  {user.avatar ? (
                    <img
                      src={user.avatar} alt={user.username} className="w-8 h-8 rounded-full" />
                    ) : (
                      <UserCircle className="w-8 h-8 text-text-muted" />
                    )}
                  <ChevronDown className="w-4 h-4 text-text-muted" />
                </button>

                {/* Dropdown Menu */}
                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-56 bg-surface border border-border rounded-lg shadow-lg py-1 z-50">
                    <div className="px-4 py-3 border-b border-border">
                      <p className="text-sm font-medium text-text">{user.username}</p>
                      {user.email && (
                        <p className="text-xs text-text-muted mt-1">{user.email}</p>
                      )}
                    </div>
                    <Link
                      to="/profile"
                      onClick={() => setShowUserMenu(false)}
                      className="flex items-center gap-2 px-4 py-2 text-sm text-text hover:bg-background transition-colors"
                    >
                      <User className="w-4 h-4" />
                      <span>个人中心</span>
                    </Link>
                    {isAdmin && (
                      <Link
                        to="/admin"
                        onClick={() => setShowUserMenu(false)}
                        className="flex items-center gap-2 px-4 py-2 text-sm text-text hover:bg-background transition-colors"
                      >
                        <Settings className="w-4 h-4" />
                        <span>管理后台</span>
                      </Link>
                    )}
                    <div className="border-t border-border my-1" />
                    <button
                      onClick={() => {
                        setShowUserMenu(false);
                        logout();
                      }}
                      className="flex items-center gap-2 px-4 py-2 text-sm text-danger hover:bg-background transition-colors w-full"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>退出登录</span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link
                to="/"
                onClick={(e) => {
                  e.preventDefault();
                  // 这里可以打开登录模态框，暂时先不处理
                }}
                className="flex items-center gap-2 text-sm font-medium text-text hover:text-primary transition-colors"
              >
                <LogIn className="w-4 h-4" />
                <span className="hidden sm:inline">登录</span>
              </Link>
            )}

            {/* Mobile Menu Button */}
            <button
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-md hover:bg-background"
            >
              {isMenuOpen ? (
                <X className="h-6 w-6 text-text" />
              ) : (
                <Menu className="h-6 w-6 text-text" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Search Bar */}
      {showSearch && (
        <div className="border-t border-border">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <SearchBar onSearch={() => setShowSearch(false)} />
          </div>
        </div>
      )}

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden border-t border-border bg-surface">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsMenuOpen(false)}
                className={`block px-3 py-2 rounded-md text-base font-medium ${
                  isActive(item.path)
                    ? 'bg-primary/10 text-primary'
                    : 'text-text hover:bg-background'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
