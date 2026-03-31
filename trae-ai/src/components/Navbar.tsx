import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface NavbarProps {
  onLoginClick: () => void;
  onRegisterClick: () => void;
  showHome?: boolean;
  onHomeClick?: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ 
  onLoginClick, 
  onRegisterClick, 
  showHome = false,
  onHomeClick 
}) => {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleLogout = () => {
    logout();
    setShowUserMenu(false);
    navigate('/');
  };

  return (
    <nav className="bg-surface border-b border-border sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            {showHome ? (
              <button
                onClick={onHomeClick}
                className="text-2xl font-bold text-primary hover:text-primary/80 transition-colors"
              >
                雾漫林间动漫
              </button>
            ) : (
              <Link to="/" className="text-2xl font-bold text-primary hover:text-primary/80 transition-colors">
·                漫雾林间动漫
              </Link>
            )}
          </div>
          
          <div className="flex items-center gap-6">
            <Link 
              to="/" 
              className="text-text hover:text-primary transition-colors"
            >
              首页
            </Link>
            <Link 
              to="/ranking" 
              className="text-text hover:text-primary transition-colors"
            >
              动漫排行
            </Link>
            <Link 
              to="/recent" 
              className="text-text hover:text-primary transition-colors"
            >
              新番动漫
            </Link>
            <Link 
              to="/ongoing" 
              className="text-text hover:text-primary transition-colors"
            >
              连载动漫
            </Link>
            <Link 
              to="/completed" 
              className="text-text hover:text-primary transition-colors"
            >
              完结动漫
            </Link>
            <Link 
              to="/chinese" 
              className="text-text hover:text-primary transition-colors"
            >
              国产动漫
            </Link>
            <Link 
              to="/japanese" 
              className="text-text hover:text-primary transition-colors"
            >
              日本动漫
            </Link>
            <Link 
              to="/theater" 
              className="text-text hover:text-primary transition-colors"
            >
              剧场版
            </Link>
            <Link 
              to="/daily" 
              className="text-text hover:text-primary transition-colors"
            >
              每日推荐
            </Link>
          </div>

          <div className="flex items-center gap-4">
            <Link
              to="/search"
              className="flex items-center gap-2 px-4 py-2 bg-background border border-border rounded-full text-text hover:border-primary transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span>搜索</span>
            </Link>
            
            {user ? (
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 px-4 py-2 bg-primary/10 border border-primary/20 rounded-full text-text hover:bg-primary/20 transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                    <span className="text-white font-medium">
                      {user.username.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span>{user.username}</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-surface border border-border rounded-lg shadow-lg z-50">
                    <div className="py-2">
                      {isAdmin && (
                        <Link
                          to="/admin"
                          className="block px-4 py-2 text-text hover:bg-background"
                          onClick={() => setShowUserMenu(false)}
                        >
                          管理后台
                        </Link>
                      )}
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-text hover:bg-background"
                      >
                        退出登录
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <button
                  onClick={onLoginClick}
                  className="px-4 py-2 text-text hover:text-primary transition-colors"
                >
                  登录
                </button>
                <button
                  onClick={onRegisterClick}
                  className="px-4 py-2 bg-primary text-white rounded-full hover:bg-primary/90 transition-colors"
                >
                  注册
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
