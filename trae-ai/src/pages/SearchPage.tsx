import { useState, useEffect } from 'react';
import type { Anime } from '../types';
import SearchBar from '../components/SearchBar';
import SearchFilter from '../components/SearchFilter';
import AnimeCard from '../components/AnimeCard';
import AnimeDetailModal from '../components/AnimeDetailModal';

interface FilterOptions {
  years: number[];
  statuses: string[];
  studios: string[];
}

const SearchPage: React.FC = () => {
  const [searchResults, setSearchResults] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    years: [],
    statuses: [],
    studios: [],
  });
  
  // 筛选状态
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<string | null>(null);
  const [selectedStudio, setSelectedStudio] = useState<string | null>(null);
  const [currentKeyword, setCurrentKeyword] = useState('');
  
  // 分页
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  
  // 动漫详情
  const [selectedAnime, setSelectedAnime] = useState<Anime | null>(null);
  const [showAnimeDetail, setShowAnimeDetail] = useState(false);

  // 获取筛选选项
  useEffect(() => {
    const fetchFilterOptions = async () => {
      try {
        const response = await fetch('/api/anime/filter-options');
        const data = await response.json();
        setFilterOptions(data.data || data);
      } catch (error) {
        console.error('Failed to fetch filter options:', error);
      }
    };

    fetchFilterOptions();
  }, []);

  // 搜索函数
  const performSearch = async (
    keyword: string,
    year: number | null = null,
    status: string | null = null,
    studio: string | null = null,
    page: number = 1
  ) => {
    setIsLoading(true);
    
    try {
      let url = `/api/anime/search?page=${page}&limit=12`;
      
      if (keyword.trim()) {
        url += `&keyword=${encodeURIComponent(keyword)}`;
      }
      if (year) {
        url += `&year=${year}`;
      }
      if (status) {
        url += `&status=${encodeURIComponent(status)}`;
      }
      if (studio) {
        url += `&studio=${encodeURIComponent(studio)}`;
      }

      const response = await fetch(url);
      const result = await response.json();
      const data = result.data || result;
      
      setSearchResults(data.animes || []);
      setTotalPages(data.pagination?.totalPages || 1);
      setTotalResults(data.pagination?.total || 0);
      setCurrentPage(page);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (keyword: string) => {
    setCurrentKeyword(keyword);
    setHasSearched(true);
    setShowFilters(true);
    performSearch(keyword, selectedYear, selectedStatus, selectedStudio, 1);
  };

  const handleYearChange = (year: number | null) => {
    setSelectedYear(year);
    setHasSearched(true);
    performSearch(currentKeyword, year, selectedStatus, selectedStudio, 1);
  };

  const handleStatusChange = (status: string | null) => {
    setSelectedStatus(status);
    setHasSearched(true);
    performSearch(currentKeyword, selectedYear, status, selectedStudio, 1);
  };

  const handleStudioChange = (studio: string | null) => {
    setSelectedStudio(studio);
    setHasSearched(true);
    performSearch(currentKeyword, selectedYear, selectedStatus, studio, 1);
  };

  const handleResetFilters = () => {
    setSelectedYear(null);
    setSelectedStatus(null);
    setSelectedStudio(null);
    performSearch(currentKeyword, null, null, null, 1);
  };

  const handlePageChange = (page: number) => {
    performSearch(currentKeyword, selectedYear, selectedStatus, selectedStudio, page);
  };

  const handleAnimeClick = (anime: Anime) => {
    setSelectedAnime(anime);
    setShowAnimeDetail(true);
  };

  // 生成分页页码（优化显示）
  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;
    
    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      if (currentPage <= 3) {
        for (let i = 1; i <= maxVisible; i++) {
          pages.push(i);
        }
      } else if (currentPage >= totalPages - 2) {
        for (let i = totalPages - maxVisible + 1; i <= totalPages; i++) {
          pages.push(i);
        }
      } else {
        for (let i = currentPage - 2; i <= currentPage + 2; i++) {
          pages.push(i);
        }
      }
    }
    
    return pages;
  };

  // 初始加载时显示所有动漫，但不显示筛选条件
  useEffect(() => {
    const initialLoad = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('/api/anime/search?page=1&limit=12');
        const result = await response.json();
        const data = result.data || result;
        
        setSearchResults(data.animes || []);
        setTotalPages(data.pagination?.totalPages || 1);
        setTotalResults(data.pagination?.total || 0);
        setCurrentPage(1);
      } catch (error) {
        console.error('Initial load failed:', error);
        setSearchResults([]);
      } finally {
        setIsLoading(false);
      }
    };
    
    initialLoad();
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 搜索区域 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-text mb-4">发现精彩动漫</h1>
          <p className="text-text-muted mb-8">
            搜索你喜欢的动漫，或使用筛选条件发现新作品
          </p>
          <div className="flex justify-center">
            <SearchBar onSearch={handleSearch} />
          </div>
        </div>

        {/* 筛选区域 */}
        {showFilters && (
          <SearchFilter
            years={filterOptions.years}
            statuses={filterOptions.statuses}
            studios={filterOptions.studios}
            selectedYear={selectedYear}
            selectedStatus={selectedStatus}
            selectedStudio={selectedStudio}
            onYearChange={handleYearChange}
            onStatusChange={handleStatusChange}
            onStudioChange={handleStudioChange}
            onReset={handleResetFilters}
          />
        )}

        {/* 显示筛选按钮 */}
        {!showFilters && (
          <div className="text-center mb-8">
            <button
              onClick={() => setShowFilters(true)}
              className="px-6 py-2 bg-surface border border-border rounded-lg text-text hover:border-primary/50 transition-colors"
            >
              显示筛选条件
            </button>
          </div>
        )}

        {/* 搜索结果统计 */}
        {hasSearched && (
          <div className="flex items-center justify-between mb-6">
            <p className="text-text-muted">
              {currentKeyword ? (
                <>搜索 "<span className="text-text font-medium">{currentKeyword}</span>" 的结果</>
              ) : (
                <>全部动漫</>
              )}
              <span className="ml-2">({totalResults} 个结果)</span>
            </p>
          </div>
        )}

        {/* 搜索结果列表 */}
        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-text-muted">搜索中...</div>
          </div>
        ) : searchResults.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-text-muted mb-4">
              {hasSearched ? '没有找到相关动漫' : '暂无数据'}
            </div>
            <p className="text-sm text-text-muted">
              尝试使用其他关键词或调整筛选条件
            </p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {searchResults.map((anime) => (
                <AnimeCard
                  key={anime.id}
                  anime={anime}
                  onClick={() => handleAnimeClick(anime)}
                />
              ))}
            </div>

            {/* 分页 */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
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
                        page === currentPage
                          ? 'bg-primary text-white'
                          : 'bg-surface border border-border text-text hover:border-primary/50'
                      }`}
                    >
                      {page}
                    </button>
                  ))}
                </div>

                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 bg-surface border border-border rounded-lg text-text disabled:opacity-50 disabled:cursor-not-allowed hover:border-primary/50 transition-colors"
                >
                  下一页
                </button>
              </div>
            )}
          </>
        )}
      </main>

      {/* 动漫详情弹窗 */}
      <AnimeDetailModal
        isOpen={showAnimeDetail}
        onClose={() => {
          setShowAnimeDetail(false);
          setSelectedAnime(null);
        }}
        anime={selectedAnime}
      />
    </div>
  );
};

export default SearchPage;
