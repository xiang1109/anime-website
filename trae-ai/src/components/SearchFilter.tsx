interface SearchFilterProps {
  years: number[];
  statuses: string[];
  studios: string[];
  selectedYear: number | null;
  selectedStatus: string | null;
  selectedStudio: string | null;
  onYearChange: (year: number | null) => void;
  onStatusChange: (status: string | null) => void;
  onStudioChange: (studio: string | null) => void;
  onReset: () => void;
}

const SearchFilter: React.FC<SearchFilterProps> = ({
  years,
  statuses,
  studios,
  selectedYear,
  selectedStatus,
  selectedStudio,
  onYearChange,
  onStatusChange,
  onStudioChange,
  onReset,
}) => {
  const hasActiveFilters = selectedYear || selectedStatus || selectedStudio;

  return (
    <div className="bg-surface border border-border rounded-xl p-6 mb-8">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-text">筛选条件</h3>
        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="text-sm text-primary hover:text-primary/80 transition-colors"
          >
            重置筛选
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* 年份筛选 */}
        <div>
          <label className="block text-sm font-medium text-text mb-2">
            年份
          </label>
          <select
            value={selectedYear || ''}
            onChange={(e) => onYearChange(e.target.value ? Number(e.target.value) : null)}
            className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="">全部年份</option>
            {years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>

        {/* 状态筛选 */}
        <div>
          <label className="block text-sm font-medium text-text mb-2">
            状态
          </label>
          <select
            value={selectedStatus || ''}
            onChange={(e) => onStatusChange(e.target.value || null)}
            className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="">全部状态</option>
            {statuses.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
        </div>

        {/* 工作室筛选 */}
        <div>
          <label className="block text-sm font-medium text-text mb-2">
            工作室
          </label>
          <select
            value={selectedStudio || ''}
            onChange={(e) => onStudioChange(e.target.value || null)}
            className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="">全部工作室</option>
            {studios.map((studio) => (
              <option key={studio} value={studio}>
                {studio}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default SearchFilter;
