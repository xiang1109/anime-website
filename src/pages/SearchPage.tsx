import { useState, useEffect } from 'react';
import type { Anime } from '../types';
import SearchBar from '../components/SearchBar';
import SearchFilter from '../components/SearchFilter';
import AnimeCard from '../components/AnimeCard';
import AnimeDetailModal from '../components/AnimeDetailModal';
import API_BASE_URL from '../config/api';

interface FilterOptions {
  years: number[];
  statuses: string[];
  studios: string[];
  authors: string[];
}

const SearchPage: React.FC = () => {
  const [searchResults, setSearchResults] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    years: [],
    statuses: [],
    studios: [],
    authors: [],
  });
  
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<string | null>(null);
  const [selectedStudio, setSelectedStudio] = useState<string | null>(null);
  const [selectedAuthor, setSelectedAuthor] = useState<string | null>(null);
  const [selectedStartYear, setSelectedStartYear] = useState<number | null>(null);
  const [selectedEndYear, setSelectedEndYear] = useState<number | null>(null);
  const [currentKeyword, setCurrentKeyword] = useState('');
  
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  
  const [selectedAnime, setSelectedAnime] = useState<Anime | null>(null);
  const [showAnimeDetail, setShowAnimeDetail] = useState(false);

  useEffect(() => {
    const fetchFilterOptions = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/anime/filter-options`);
        const data = await response.json();
        setFilterOptions(data.data || data);
      } catch (error) {
        console.error('Failed to fetch filter options:', error);
        setFilterOptions({
          years: [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015],
          statuses: ['连载中', '完结'],
          studios: ['雾漫动画', '樱花动画', '星际动画', '魔法动画', '机械动画', '忍者动画', '校园动画', '武侠动画', '侦探动画', '奇幻动画', '运动动画', '科幻动画'],
          authors: ['尾田荣一郎', '岸本齐史', '鸟山明', '宫崎骏', '新海诚', '手冢治虫', '高桥留美子', '富坚义博', '荒川弘', '藤本树']
        });
      }
    };

    fetchFilterOptions();
    fetchAnimeData();
  }, []);

  const fetchAnimeData = async () => {
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/anime?page=1&limit=12`);
      const result = await response.json();
      const data = result.data || result;
      
      setSearchResults(data.animes || []);
      setTotalPages(data.pagination?.totalPages || 1);
      setCurrentPage(1);
    } catch (error) {
      console.error('Failed to fetch anime data:', error);
      setSearchResults([]);
      setTotalPages(1);
    } finally {
      setIsLoading(false);
    }
  };

  const performSearch = async (
    keyword: string,
    year: number | null = null,
    status: string | null = null,
    studio: string | null = null,
    author: string | null = null,
    startYear: number | null = null,
    endYear: number | null = null,
    page: number = 1
  ) => {
    setIsLoading(true);
    
    try {
      let url = `${API_BASE_URL}/api/anime/search?page=${page}&limit=12`;
      
      if (keyword.trim()) {
        url += `&keyword=${encodeURIComponent(keyword)}`;
      }
      if (year) {
        url += `&year=${year}`;
      }
      if (startYear) {
        url += `&startYear=${startYear}`;
      }
      if (endYear) {
        url += `&endYear=${endYear}`;
      }
      if (status) {
        url += `&status=${encodeURIComponent(status)}`;
      }
      if (studio) {
        url += `&studio=${encodeURIComponent(studio)}`;
      }
      if (author) {
        url += `&author=${encodeURIComponent(author)}`;
      }

      const response = await fetch(url);
      const result = await response.json();
      const data = result.data || result;
      
      setSearchResults(data.animes || []);
      setTotalPages(data.pagination?.totalPages || 1);
      setCurrentPage(page);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
      setTotalPages(1);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (keyword: string) => {
    setCurrentKeyword(keyword);
    setShowFilters(true);
    setCurrentPage(1);
    performSearch(keyword, selectedYear, selectedStatus, selectedStudio, selectedAuthor, selectedStartYear, selectedEndYear, 1);
  };

  const handleFilterChange = (
    year: number | null, 
    status: string | null, 
    studio: string | null,
    author: string | null,
    startYear: number | null,
    endYear: number | null
  ) => {
    setSelectedYear(year);
    setSelectedStatus(status);
    setSelectedStudio(studio);
    setSelectedAuthor(author);
    setSelectedStartYear(startYear);
    setSelectedEndYear(endYear);
    setCurrentPage(1);
    performSearch(currentKeyword, year, status, studio, author, startYear, endYear, 1);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    performSearch(currentKeyword, selectedYear, selectedStatus, selectedStudio, selectedAuthor, selectedStartYear, selectedEndYear, page);
  };

  const handleResetFilters = () => {
    setSelectedYear(null);
    setSelectedStatus(null);
    setSelectedStudio(null);
    setSelectedAuthor(null);
    setSelectedStartYear(null);
    setSelectedEndYear(null);
    setCurrentPage(1);
    performSearch(currentKeyword, null, null, null, null, null, null, 1);
  };

  return (
    <div className="min-h-screen bg-background">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text mb-2">搜索你喜欢的作品</h1>
          <p className="text-text-muted">输入动漫名称、描述或其他关键词进行搜索</p>
        </div>

        <div className="mb-6">
          <SearchBar onSearch={handleSearch} />
        </div>

        {showFilters && (
          <SearchFilter
            years={filterOptions.years}
            statuses={filterOptions.statuses}
            studios={filterOptions.studios}
            authors={filterOptions.authors}
            selectedYear={selectedYear}
            selectedStatus={selectedStatus}
            selectedStudio={selectedStudio}
            selectedAuthor={selectedAuthor}
            selectedStartYear={selectedStartYear}
            selectedEndYear={selectedEndYear}
            onYearChange={(year) => handleFilterChange(year, selectedStatus, selectedStudio, selectedAuthor, selectedStartYear, selectedEndYear)}
            onStatusChange={(status) => handleFilterChange(selectedYear, status, selectedStudio, selectedAuthor, selectedStartYear, selectedEndYear)}
            onStudioChange={(studio) => handleFilterChange(selectedYear, selectedStatus, studio, selectedAuthor, selectedStartYear, selectedEndYear)}
            onAuthorChange={(author) => handleFilterChange(selectedYear, selectedStatus, selectedStudio, author, selectedStartYear, selectedEndYear)}
            onStartYearChange={(startYear) => handleFilterChange(selectedYear, selectedStatus, selectedStudio, selectedAuthor, startYear, selectedEndYear)}
            onEndYearChange={(endYear) => handleFilterChange(selectedYear, selectedStatus, selectedStudio, selectedAuthor, selectedStartYear, endYear)}
            onReset={handleResetFilters}
          />
        )}

        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4" />
            <p className="text-text-muted">加载中...</p>
          </div>
        ) : searchResults.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-text-muted">没有找到匹配的动漫</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {searchResults.map((anime) => (
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

            {totalPages > 1 && (
              <div className="flex justify-center items-center gap-4">
                <button
                  onClick={() => handlePageChange(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 bg-primary text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-hover transition-colors"
                >
                  上一页
                </button>
                <span className="text-text-muted">
                  第 {currentPage} 页，共 {totalPages} 页
                </span>
                <button
                  onClick={() => handlePageChange(Math.min(totalPages, currentPage + 1))}
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

      <AnimeDetailModal
        isOpen={showAnimeDetail}
        onClose={() => setShowAnimeDetail(false)}
        anime={selectedAnime}
      />
    </div>
  );
};

export default SearchPage;
