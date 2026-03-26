import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

interface NavbarProps {
  onLoginClick: () => void;
  onRegisterClick: () => void;
  onSearchClick?: () => void;
  showHome?: boolean;
  onHomeClick?: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ 
  onLoginClick, 
  onRegisterClick, 
  onSearchClick,
  showHome = false,
  onHomeClick 
}) => {
  const { user, logout, isAdmin } = useAuth();

  return (
    <nav className="bg-surface border-b border-border sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <svg className="w-8 h-8 text-primary" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <span className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              动漫评分
            </span>
          </div>

          {/* 导航链接 */}
          <div className="flex items-center gap-6">
            {showHome && onHomeClick && (
              <button
                onClick={onHomeClick}
                className="text-text-muted hover:text-text transition-colors text-sm font-medium"
              >
                首页
              </button>
            )}
            {!showHome && (
              <Link
                to="/"
                className="text-text-muted hover:text-text transition-colors text-sm font-medium"
              >
                首页
              </Link>
            )}
            {onSearchClick && (
              <button
                onClick={onSearchClick}
                className="text-text-muted hover:text-text transition-colors text-sm font-medium"
              >
                搜索
              </button>
            )}
            {!onSearchClick && (
              <Link
                to="/search"
                className="text-text-muted hover:text-text transition-colors text-sm font-medium"
              >
                搜索
              </Link>
            )}
            {isAdmin && (
              <Link
                to="/admin"
                className="text-primary hover:text-primary/80 transition-colors text-sm font-medium flex items-center gap-1"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                管理后台
              </Link>
            )}
          </div>

          <div className="flex items-center gap-4">
            {user ? (
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {user.username.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span className="text-text text-sm font-medium">{user.username}</span>
                </div>
                <button
                  onClick={logout}
                  className="px-4 py-2 text-sm text-text-muted hover:text-text transition-colors"
                >
                  退出登录
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <button
                  onClick={onLoginClick}
                  className="px-4 py-2 text-sm text-text hover:text-primary transition-colors"
                >
                  登录
                </button>
                <button
                  onClick={onRegisterClick}
                  className="btn-primary px-4 py-2 text-sm text-white rounded-lg"
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
