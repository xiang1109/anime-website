interface SearchFilterProps {
  years: number[];
  statuses: string[];
  studios: string[];
  authors: string[];
  selectedYear: number | null;
  selectedStatus: string | null;
  selectedStudio: string | null;
  selectedAuthor: string | null;
  selectedStartYear: number | null;
  selectedEndYear: number | null;
  onYearChange: (year: number | null) => void;
  onStatusChange: (status: string | null) => void;
  onStudioChange: (studio: string | null) => void;
  onAuthorChange: (author: string | null) => void;
  onStartYearChange: (year: number | null) => void;
  onEndYearChange: (year: number | null) => void;
  onReset: () => void;
}

const SearchFilter: React.FC<SearchFilterProps> = ({
  years,
  statuses,
  studios,
  authors,
  selectedYear,
  selectedStatus,
  selectedStudio,
  selectedAuthor,
  selectedStartYear,
  selectedEndYear,
  onYearChange,
  onStatusChange,
  onStudioChange,
  onAuthorChange,
  onStartYearChange,
  onEndYearChange,
  onReset,
}) => {
  const hasActiveFilters = selectedYear || selectedStatus || selectedStudio || selectedAuthor || selectedStartYear || selectedEndYear;

  return (
    <div className="bg-surface/80 backdrop-blur-sm border border-border/50 rounded-2xl p-6 mb-8 shadow-lg">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center">
            <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-text">筛选条件</h3>
        </div>
        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="flex items-center gap-2 px-4 py-2 text-sm text-primary hover:text-primary/80 bg-primary/10 hover:bg-primary/20 rounded-lg transition-all duration-300"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            重置筛选
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* 单年份筛选 */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-text">
            <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            特定年份
          </label>
          <select
            value={selectedYear || ''}
            onChange={(e) => onYearChange(e.target.value ? Number(e.target.value) : null)}
            className="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl text-text focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50 transition-all duration-300 hover:border-primary/30"
          >
            <option value="">不限制</option>
            {years.map((year) => (
              <option key={year} value={year}>
                {year}年
              </option>
            ))}
          </select>
        </div>

        {/* 起始年份 */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-text">
            <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
            </svg>
            起始年份
          </label>
          <select
            value={selectedStartYear || ''}
            onChange={(e) => onStartYearChange(e.target.value ? Number(e.target.value) : null)}
            className="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl text-text focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50 transition-all duration-300 hover:border-primary/30"
          >
            <option value="">不限</option>
            {years.map((year) => (
              <option key={`start-${year}`} value={year}>
                {year}年及以后
              </option>
            ))}
          </select>
        </div>

        {/* 结束年份 */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-text">
            <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            结束年份
          </label>
          <select
            value={selectedEndYear || ''}
            onChange={(e) => onEndYearChange(e.target.value ? Number(e.target.value) : null)}
            className="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl text-text focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50 transition-all duration-300 hover:border-primary/30"
          >
            <option value="">不限</option>
            {years.map((year) => (
              <option key={`end-${year}`} value={year}>
                {year}年及以前
              </option>
            ))}
          </select>
        </div>

        {/* 状态 */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-text">
            <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            状态
          </label>
          <select
            value={selectedStatus || ''}
            onChange={(e) => onStatusChange(e.target.value || null)}
            className="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl text-text focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50 transition-all duration-300 hover:border-primary/30"
          >
            <option value="">全部状态</option>
            {statuses.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
        </div>

        {/* 工作室 */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-text">
            <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            工作室
          </label>
          <select
            value={selectedStudio || ''}
            onChange={(e) => onStudioChange(e.target.value || null)}
            className="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl text-text focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50 transition-all duration-300 hover:border-primary/30"
          >
            <option value="">全部工作室</option>
            {studios.map((studio) => (
              <option key={studio} value={studio}>
                {studio}
              </option>
            ))}
          </select>
        </div>

        {/* 作者 */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-text">
            <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            作者
          </label>
          <select
            value={selectedAuthor || ''}
            onChange={(e) => onAuthorChange(e.target.value || null)}
            className="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl text-text focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50 transition-all duration-300 hover:border-primary/30"
          >
            <option value="">全部作者</option>
            {authors.map((author) => (
              <option key={author} value={author}>
                {author}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default SearchFilter;