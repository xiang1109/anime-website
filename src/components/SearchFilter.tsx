import React from 'react';

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
  years = [],
  statuses = [],
  studios = [],
  authors = [],
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
    <div className="bg-surface/80 backdrop-blur-xl border border-white/10 rounded-3xl p-7 mb-8 shadow-2xl relative overflow-hidden">
      {/* 装饰性背景 */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-20 -right-20 w-40 h-40 bg-pink-500/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-20 -left-20 w-40 h-40 bg-cyan-500/10 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-7">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-pink-500/20 via-purple-500/20 to-cyan-500/20 flex items-center justify-center border border-white/10">
              <svg className="w-6 h-6 text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">筛选条件</h3>
              <p className="text-xs text-white/50 mt-1">精准找到你想看的动漫</p>
            </div>
          </div>
          {hasActiveFilters && (
            <button
              onClick={onReset}
              className="flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-cyan-400 hover:from-pink-300 hover:to-cyan-300 bg-white/5 hover:bg-white/10 rounded-xl transition-all"
            >
              <svg className="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              重置筛选
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {/* 单年份筛选 */}
          <div className="space-y-2.5">
            <label className="flex items-center gap-2 text-sm font-semibold text-white/90">
              <svg className="w-4 h-4 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              特定年份
            </label>
            <select
              value={selectedYear || ''}
              onChange={(e) => onYearChange(e.target.value ? Number(e.target.value) : null)}
              className="w-full px-4 py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-pink-500/40 focus:border-pink-500/40 transition-all hover:border-white/20"
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
          <div className="space-y-2.5">
            <label className="flex items-center gap-2 text-sm font-semibold text-white/90">
              <svg className="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
              起始年份
            </label>
            <select
              value={selectedStartYear || ''}
              onChange={(e) => onStartYearChange(e.target.value ? Number(e.target.value) : null)}
              className="w-full px-4 py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/40 focus:border-purple-500/40 transition-all hover:border-white/20"
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
          <div className="space-y-2.5">
            <label className="flex items-center gap-2 text-sm font-semibold text-white/90">
              <svg className="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              结束年份
            </label>
            <select
              value={selectedEndYear || ''}
              onChange={(e) => onEndYearChange(e.target.value ? Number(e.target.value) : null)}
              className="w-full px-4 py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-cyan-500/40 focus:border-cyan-500/40 transition-all hover:border-white/20"
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
          <div className="space-y-2.5">
            <label className="flex items-center gap-2 text-sm font-semibold text-white/90">
              <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              状态
            </label>
            <select
              value={selectedStatus || ''}
              onChange={(e) => onStatusChange(e.target.value || null)}
              className="w-full px-4 py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-green-500/40 focus:border-green-500/40 transition-all hover:border-white/20"
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
          <div className="space-y-2.5">
            <label className="flex items-center gap-2 text-sm font-semibold text-white/90">
              <svg className="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              工作室
            </label>
            <select
              value={selectedStudio || ''}
              onChange={(e) => onStudioChange(e.target.value || null)}
              className="w-full px-4 py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-yellow-500/40 focus:border-yellow-500/40 transition-all hover:border-white/20"
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
          <div className="space-y-2.5">
            <label className="flex items-center gap-2 text-sm font-semibold text-white/90">
              <svg className="w-4 h-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              作者
            </label>
            <select
              value={selectedAuthor || ''}
              onChange={(e) => onAuthorChange(e.target.value || null)}
              className="w-full px-4 py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-orange-500/40 focus:border-orange-500/40 transition-all hover:border-white/20"
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
    </div>
  );
};

export default SearchFilter;
