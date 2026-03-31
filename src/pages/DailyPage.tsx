import { useState, useEffect } from 'react';
import AnimeListPage from '../components/AnimeListPage';
import AnimeCard from '../components/AnimeCard';
import API_BASE_URL from '../config/api';
import type { Anime } from '../types';

const DailyPage: React.FC = () => {
  const [hiddenGems, setHiddenGems] = useState<Anime[]>([]);
  const [isLoadingGems, setIsLoadingGems] = useState(true);

  useEffect(() => {
    fetchHiddenGems();
  }, []);

  const fetchHiddenGems = async () => {
    setIsLoadingGems(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/anime/hidden-gems`);
      const result = await response.json();
      const data = result.data || result;
      setHiddenGems(data.animes || data.data || []);
    } catch (error) {
      console.error('Failed to fetch hidden gems:', error);
      setHiddenGems([]);
    } finally {
      setIsLoadingGems(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* B站冷门佳作 */}
        <section className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-3xl font-bold text-foreground mb-2">
                Table冷门佳作
              </h2>
              <p className="text-muted-foreground">
                来自B站的高分冷门动漫，不容错过的宝藏作品
              </p>
            </div>
          </div>

          {isLoadingGems ? (
            <div className="text-center py-8">
              <div className="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4" />
              <p className="text-muted-foreground">加载中...</p>
            </div>
          ) : hiddenGems.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">暂无数据</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {hiddenGems.map((anime) => (
                <AnimeCard
                  key={anime.id}
                  anime={anime}
                  linkToDetail={true}
                />
              ))}
            </div>
          )}
        </section>

        {/* 每日推荐 */}
        <section>
          <AnimeListPage
            title="每日推荐"
            description="每日精选推荐动漫"
            apiEndpoint="/api/anime/daily"
          />
        </section>
      </main>
    </div>
  );
};

export default DailyPage;
