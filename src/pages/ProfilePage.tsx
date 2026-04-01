import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProfilePage: React.FC = () => {
  const { user, logout } = useAuth();

  if (!user) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-text-muted mb-4">请先登录</p>
          <Link
            to="/"
            className="text-primary hover:underline"
          >
            返回首页
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 用户信息卡片 */}
        <div className="bg-surface rounded-xl p-6 border border-border shadow-lg mb-8">
          <div className="flex items-start gap-6">
            <div className="flex-shrink-0">
              <div className="w-24 h-24 rounded-full bg-primary/20 flex items-center justify-center">
                <span className="text-text-muted text-2xl">👤</span>
              </div>
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-text mb-2">{user.username}</h1>
              {user.email && (
                <p className="text-text-muted mb-4">{user.email}</p>
              )}
              <div className="flex flex-wrap gap-3">
                <button className="flex items-center gap-2 px-4 py-2 bg-background text-text rounded-lg hover:bg-background/80 transition-colors">
                  <span>⚙️</span>
                  <span>编辑资料</span>
                </button>
                <button
                  onClick={logout}
                  className="flex items-center gap-2 px-4 py-2 bg-danger text-white rounded-lg hover:bg-danger/90 transition-colors"
                >
                  <span>🚪</span>
                  <span>退出登录</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* 评分记录 */}
        <div className="bg-surface rounded-xl p-6 border border-border shadow-lg">
          <h2 className="text-xl font-bold text-text mb-4">我的评分</h2>
          <div className="text-center py-8">
            <p className="text-text-muted">还没有评分记录</p>
            <Link
              to="/"
              className="text-primary hover:underline mt-2 inline-block"
            >
              去发现动漫
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ProfilePage;
