import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import API_BASE_URL from '../config/api';
import type { Anime } from '../types';
import AnimeCard from '../components/AnimeCard';
import AnimeDetailModal from '../components/AnimeDetailModal';
import { User, Settings, LogOut } from 'lucide-react';

const ProfilePage: React.FC = () => {
  const { user, logout, token } = useAuth();
  const [ratedAnimes, setRatedAnimes] = useState<Anime[]>([]);
  const [selectedAnime, setSelectedAnime] = useState<Anime | null>(null);
  const [showAnimeDetail, setShowAnimeDetail] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // 这里可以获取用户评分过的动漫列表
    // 暂时先留空，后续可以添加API
    setIsLoading(false);
  }, [token]);

  if (!user) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">请先登录</p>
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
        <div className="bg-card rounded-xl p-6 border border-border shadow-lg mb-8">
          <div className="flex items-start gap-6">
            <div className="flex-shrink-0">
              {user.avatar ? (
                <img
                  src={user.avatar}
                  alt={user.username}
                  className="w-24 h-24 rounded-full"
                />
              ) : (
                <div className="w-24 h-24 rounded-full bg-primary/20 flex items-center justify-center">
                  <User className="w-12 h-12 text-primary" />
                </div>
              )}
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-foreground mb-2">{user.username}</h1>
              {user.email && (
                <p className="text-muted-foreground mb-4">{user.email}</p>
              )}
              <div className="flex flex-wrap gap-3">
                <button className="flex items-center gap-2 px-4 py-2 bg-muted text-foreground rounded-lg hover:bg-muted/80 transition-colors">
                  <Settings className="w-4 h-4" />
                  <span>编辑资料</span>
                </button>
                <button
                  onClick={logout}
                  className="flex items-center gap-2 px-4 py-2 bg-destructive text-destructive-foreground rounded-lg hover:bg-destructive/90 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span>退出登录</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* 评分记录 */}
        <div className="bg-card rounded-xl p-6 border border-border shadow-lg">
          <h2 className="text-xl font-bold text-foreground mb-4">我的评分</h2>
          {isLoading ? (
            <div className="text-center py-8">
              <div className="inline-block w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin mb-2" />
              <p className="text-muted-foreground">加载中...</p>
            </div>
          ) : ratedAnimes.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">还没有评分记录</p>
              <Link
                to="/"
                className="text-primary hover:underline mt-2 inline-block"
              >
                去发现动漫
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {ratedAnimes.map((anime) => (
                <AnimeCard
                  key={anime.id}
                  anime={anime}
                  onClick={() => {
                    setSelectedAnime(anime);
                    setShowAnimeDetail(true);
                  }}
                />
              ))}
            </div>
          )}
        </div>
      </main>

      {selectedAnime && (
        <AnimeDetailModal
          anime={selectedAnime}
          isOpen={showAnimeDetail}
          onClose={() => {
            setShowAnimeDetail(false);
            setSelectedAnime(null);
          }}
        />
      )}
    </div>
  );
};

export default ProfilePage;
