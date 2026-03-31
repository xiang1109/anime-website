import { useState } from 'react';

interface SearchBarProps {
  onSearch: (keyword: string) => void;
  placeholder?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, placeholder = '搜索动漫...' }) => {
  const [keyword, setKeyword] = useState('');
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(keyword);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className={`relative transition-all duration-300 ${isFocused ? 'transform scale-105' : ''}`}>
        <div className={`absolute inset-0 rounded-full transition-all duration-300 ${isFocused ? 'bg-gradient-to-r from-primary/20 to-primary/10 blur-xl' : ''}`} />
        <div className="relative">
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder={placeholder}
            className={`w-full px-6 py-4 pl-14 bg-surface border-2 rounded-full text-text placeholder-text-muted focus:outline-none transition-all duration-300 ${
              isFocused 
                ? 'border-primary/80 shadow-lg shadow-primary/20' 
                : 'border-border hover:border-primary/40'
            }`}
          />
          <div className="absolute left-5 top-1/2 transform -translate-y-1/2">
            <svg
              className={`w-6 h-6 transition-all duration-300 ${isFocused ? 'text-primary' : 'text-text-muted'}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 014 0z"
              />
            </svg>
          </div>
          <button
            type="submit"
            className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 px-6 py-2.5 text-sm font-medium text-white rounded-full transition-all duration-300 hover:shadow-lg hover:shadow-primary/30 hover:scale-105 active:scale-95"
          >
            搜索
          </button>
        </div>
      </div>
    </form>
  );
};

export default SearchBar;