import { useState, useEffect } from 'react';
import type { Anime } from '../types';
import AnimeCard from './AnimeCard';
import AnimeDetailModal from './AnimeDetailModal';
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
  const [selectedAnime, setSelectedAnime] = useState<Anime | null>(null);
  const [showAnimeDetail, setShowAnimeDetail] = useState(false);

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
        {/* 标题区域 */}
        {(title || description) && (
          <div className="mb-8">
            {title && (
              <h2 className="text-3xl font-bold text-foreground mb-2">
                {title}
              </h2>
            )}
            {description && (
              <p className="text-muted-foreground">
                {description}
              </p>
            )}
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4" />
            <p className="text-muted-foreground">加载中...</p>
          </div>
        ) : animeList.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">暂无数据</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {animeList.map((anime) => (
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

            {/* 分页组件 - 显示页数 */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center gap-4 flex-wrap">
                <button
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 bg-primary text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-hover transition-colors"
                >
                  上一页
                </button>
                
                {/* 显示当前页数和总页数 */}
                <div className="flex items-center gap-2 px-4 py-2 bg-muted rounded-lg">
                  <span className="text-foreground font-medium">
                    第 {currentPage} 页
                  </span>
                  <span className="text-muted-foreground">
                    / 共 {totalPages} 页
                  </span>
                </div>
                
                <button
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 bg-primary text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-hover transition-colors"
                >
                  下一页
                </button>
              </div>
            )}
          </>
        )}
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

export default AnimeListPage;
