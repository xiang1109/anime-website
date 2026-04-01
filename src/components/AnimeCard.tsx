import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Anime } from '../types';
import StarRating from './StarRating';

interface AnimeCardProps {
  anime: Anime;
  onClick?: () => void;
  linkToDetail?: boolean;
}

const AnimeCard: React.FC<AnimeCardProps> = ({ 
  anime, 
  onClick, 
  linkToDetail = true 
}) => {
  const rating = Number(anime.average_rating);
  const displayRating = rating > 0 ? rating.toFixed(1) : 'N/A';
  const [imageError, setImageError] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);
  
  // 生成动漫主题色的占位背景
  const getPlaceholderGradient = () => {
    const colors = [
      'linear-gradient(135deg, #ff6b9d 0%, #c44cff 100%)',
      'linear-gradient(135deg, #00d4ff 0%, #0099ff 100%)',
      'linear-gradient(135deg, #7cff7c 0%, #00cc88 100%)',
      'linear-gradient(135deg, #ffd700 0%, #ff8c00 100%)',
      'linear-gradient(135deg, #ff8c00 0%, #ff4444 100%)'
    ];
    const index = anime.id % colors.length;
    return colors[index];
  };
  
  // 处理图片加载
  const handleImageLoad = () => {
    setImageLoaded(true);
  };
  
  const cardContent = (
    <div className="group h-full">
      <div className="relative overflow-hidden">
        {/* 图片占位加载 */}
        {!imageLoaded && !imageError && (
          <div 
            className="w-full h-64 flex items-center justify-center"
            style={{ background: getPlaceholderGradient() }}
          >
            <div className="text-center">
              <div className="w-10 h-10 border-3 border-white/30 border-t-white rounded-full animate-spin mx-auto mb-2" />
              <span className="text-white/70 text-sm">加载中...</span>
            </div>
          </div>
        )}
        
        {imageError ? (
          <div 
            className="w-full h-64 flex flex-col items-center justify-center"
            style={{ background: getPlaceholderGradient() }}
          >
            <span className="text-5xl mb-3">🎬</span>
            <span className="text-white text-sm font-medium text-center px-4">
              {anime.title}
            </span>
            <span className="text-white/60 text-xs mt-2">
              {anime.release_year || '未知年份'}
            </span>
          </div>
        ) : (
          <img
            src={anime.cover_image}
            alt={anime.title}
            className={`w-full h-64 object-cover transition-all duration-500 group-hover:scale-110 ${
              imageLoaded ? 'opacity-100' : 'opacity-0 absolute inset-0'
            }`}
            onError={() => setImageError(true)}
            onLoad={handleImageLoad}
            loading="lazy"
            crossOrigin="anonymous"
          />
        )}
        
        {/* 状态标签 */}
        <div className="absolute top-3 left-3 flex gap-2 flex-wrap">
          {anime.nationality && anime.nationality !== '日本' && (
            <span className={`px-2.5 py-1 text-xs font-semibold rounded-full backdrop-blur-sm ${
              anime.nationality === '国产' || anime.nationality === '中国'
                ? 'bg-emerald-500/80 text-white shadow-lg shadow-emerald-500/30' 
                : 'bg-cyan-500/80 text-white shadow-lg shadow-cyan-500/30'
            }`}>
              {anime.nationality}
            </span>
          )}
          {anime.is_movie && (
            <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-purple-500/80 text-white backdrop-blur-sm shadow-lg shadow-purple-500/30">
              剧场版
            </span>
          )}
        </div>
        
        {/* 连载/完结标签 */}
        <div className="absolute top-3 right-3">
          <span className={`px-2.5 py-1 text-xs font-semibold rounded-full backdrop-blur-sm ${
            anime.status === '连载中' 
              ? 'bg-green-500/80 text-white shadow-lg shadow-green-500/30' 
              : 'bg-white/20 text-white shadow-lg'
          }`}>
            {anime.status}
          </span>
        </div>
        
        {/* 评分标签 */}
        {rating > 0 && (
          <div className="absolute bottom-3 right-3">
            <div className="px-2.5 py-1 bg-black/50 backdrop-blur-sm rounded-full flex items-center gap-1.5 shadow-lg">
              <span className="text-yellow-400">⭐</span>
              <span className="text-white text-sm font-bold">{displayRating}</span>
            </div>
          </div>
        )}
      </div>
      
      <div className="p-4 flex flex-col flex-1">
        <h3 className="text-lg font-bold text-white mb-1.5 line-clamp-1 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-pink-400 group-hover:to-cyan-400 transition-all">
          {anime.title}
        </h3>
        
        {anime.title_jp && (
          <p className="text-xs text-white/50 mb-2 line-clamp-1">{anime.title_jp}</p>
        )}
        
        {anime.description && anime.description !== '暂无描述' && (
          <p className="text-sm text-white/60 mb-3 line-clamp-2 flex-1">{anime.description}</p>
        )}
        
        <div className="flex items-center justify-between mt-auto pt-2 border-t border-white/10">
          <div className="flex items-center gap-2">
            <StarRating rating={Math.round(rating)} size="sm" readonly />
            {rating > 0 && (
              <span className="text-sm text-white/60 font-medium">
                {displayRating}
              </span>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            {anime.studio && (
              <span className="text-xs text-white/40 hidden sm:block">
                {anime.studio}
              </span>
            )}
            <span className="text-sm text-white/60 font-medium bg-white/5 px-2 py-0.5 rounded-lg">
              {anime.release_year}
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  const wrapperClass = "anime-card bg-surface border border-white/10 rounded-2xl overflow-hidden transition-all duration-400 hover:border-pink-500/50 hover:shadow-2xl hover:shadow-pink-500/20 hover:-translate-y-2 flex flex-col h-full";

  if (linkToDetail) {
    return (
      <Link to={`/anime/${anime.id}`} className={wrapperClass}>
        {cardContent}
      </Link>
    );
  }

  return (
    <div className={`${wrapperClass} cursor-pointer`} onClick={onClick}>
      {cardContent}
    </div>
  );
};

export default AnimeCard;
