import { useState, useEffect } from 'react';
import type { Anime } from '../types';
import AnimeCard from './AnimeCard';
import API_BASE_URL from '../config/api';

interface AnimeListPageProps {
  title?: string;
  description?: string;
  apiEndpoint: string;
}

const AnimeListPage: React.FC<AnimeListPageProps> = ({ 
  title, 
  description, 
  apiEndpoint 
}) => {
  const [animeList, setAnimeList] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchAnimeList(currentPage);
  }, [currentPage, apiEndpoint]);

  const fetchAnimeList = async (page: number = 1) => {
    setIsLoading(true);
    try {
      const separator = apiEndpoint.includes('?') ? '&' : '?';
      const response = await fetch(`${API_BASE_URL}${apiEndpoint}${separator}page=${page}&limit=12`);
      const result = await response.json();
      const data = result.data || result;
      
      setAnimeList(data.animes || data.data || []);
      setTotalPages(data.pagination?.totalPages || 1);
    } catch (error) {
      console.error('Failed to fetch anime list:', error);
      setAnimeList([]);
      setTotalPages(1);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 标题区域 - 秒速五厘米风格 */}
        {(title || description) && (
          <div className="mb-8">
            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-pink-500/10 via-purple-500/10 to-cyan-500/10 border border-white/10 p-8 mb-6">
              {/* 装饰性背景 */}
              <div className="absolute inset-0 pointer-events-none">
                <div className="absolute -top-10 -right-10 w-32 h-32 bg-pink-500/20 rounded-full blur-3xl" />
                <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-cyan-500/20 rounded-full blur-3xl" />
              </div>
              
              <div className="relative z-10 flex items-start gap-6">
                {/* 秒速五厘米风格头像 - 男女主 */}
                <div className="flex-shrink-0">
                  <div className="relative">
                    <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center shadow-xl shadow-pink-500/30 border-2 border-white/20">
                      <span className="text-4xl">🌸</span>
                    </div>
                    <div className="absolute -bottom-2 -right-2 w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-xl shadow-cyan-500/30 border-2 border-white/20">
                      <span className="text-2xl">🚃</span>
                    </div>
                  </div>
                </div>
                
                {/* 标题和文字 */}
                <div className="flex-1">
                  {title && (
                    <h2 className="text-3xl font-bold text-white mb-2">
                      {title}
                    </h2>
                  )}
                  {description && (
                    <p className="text-text-muted mb-3">
                      {description}
                    </p>
                  )}
                  {/* 秒速五厘米风格标语 */}
                  <p className="text-sm text-pink-300/80 italic">
                    "樱花飘落的速度，是每秒五厘米..."
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4" />
            <p className="text-text-muted">加载中...</p>
          </div>
        ) : animeList.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-text-muted">暂无数据</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {animeList.map((anime) => (
                <AnimeCard
                  key={anime.id}
                  anime={anime}
                  linkToDetail={true}
                />
              ))}
            </div>

            {/* 分页组件 - 更明显的显示 */}
            <div className="border-t border-border pt-8">
              <div className="flex justify-center items-center gap-4 flex-wrap">
                <button
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="px-6 py-3 bg-primary text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-dark transition-colors font-medium"
                >
                  上一页
                </button>
                
                {/* 显示当前页数和总页数 - 更显眼 */}
                <div className="flex items-center gap-3 px-6 py-3 bg-surface border border-border rounded-lg shadow-md">
                  <span className="text-lg font-bold text-text">
                    第 {currentPage} 页
                  </span>
                  <span className="text-lg text-text-muted">
                    / 共 {totalPages} 页
                  </span>
                </div>
                
                <button
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className="px-6 py-3 bg-primary text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-dark transition-colors font-medium"
                >
                  下一页
                </button>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
};

export default AnimeListPage;
