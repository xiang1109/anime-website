import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Anime } from '../types';
import StarRating from './StarRating';
import { getAnimeCoverImage, getGradientColor } from '../utils/imageUtils';
import HoverStarEffect from './HoverStarEffect';

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
  const [isHovered, setIsHovered] = useState(false);
  
  // 使用工具函数处理图片URL
  const imageUrl = getAnimeCoverImage(anime);
  const gradientBg = getGradientColor(anime);
  
  // 处理图片加载
  const handleImageLoad = () => {
    setImageLoaded(true);
  };
  
  // 处理图片错误 - 使用多重备用方案
  const handleImageError = () => {
    if (!imageError) {
      setImageError(true);
    }
  };
  
  const cardContent = (
    <div 
      className="group h-full relative"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <HoverStarEffect isHovered={isHovered} />
      <div className="relative overflow-hidden">
        {/* 图片占位加载 */}
        <div 
          className="w-full h-64 flex items-center justify-center"
          style={{ background: gradientBg }}
        >
          {!imageLoaded && !imageError && (
            <div className="text-center">
              <div className="w-12 h-12 border-4 border-white/30 border-t-white rounded-full animate-spin mx-auto mb-3" />
              <span className="text-white/80 text-sm font-medium">加载中...</span>
            </div>
          )}
          
          {imageError ? (
            <div className="text-center">
              <span className="text-6xl mb-4 block">🎬</span>
              <span className="text-white text-base font-bold text-center px-4 block mb-2">
                {anime.title}
              </span>
              <span className="text-white/70 text-sm">
                {anime.release_year || '未知年份'}
              </span>
            </div>
          ) : (
            <img
              src={imageUrl}
              alt={anime.title}
              className={`w-full h-64 object-cover transition-all duration-700 ${
                imageLoaded ? 'opacity-100' : 'opacity-0 absolute inset-0'
              }`}
              onError={handleImageError}
              onLoad={handleImageLoad}
              loading="lazy"
              referrerPolicy="no-referrer"
            />
          )}
        </div>
        
        {/* 状态标签 */}
        <div className="absolute top-3 left-3 flex gap-2 flex-wrap">
          {anime.nationality && anime.nationality !== '日本' && (
            <span className={`px-2.5 py-1 text-xs font-bold rounded-full backdrop-blur-md ${
              anime.nationality === '国产' || anime.nationality === '中国'
                ? 'bg-emerald-500/90 text-white shadow-lg shadow-emerald-500/40' 
                : 'bg-cyan-500/90 text-white shadow-lg shadow-cyan-500/40'
            }`}>
              {anime.nationality}
            </span>
          )}
          {anime.is_movie && (
            <span className="px-2.5 py-1 text-xs font-bold rounded-full bg-purple-500/90 text-white backdrop-blur-md shadow-lg shadow-purple-500/40">
              剧场版
            </span>
          )}
        </div>
        
        {/* 连载/完结标签 */}
        <div className="absolute top-3 right-3">
          <span className={`px-2.5 py-1 text-xs font-bold rounded-full backdrop-blur-md ${
            anime.status === '连载中' 
              ? 'bg-green-500/90 text-white shadow-lg shadow-green-500/40' 
              : 'bg-white/25 text-white shadow-lg'
          }`}>
            {anime.status}
          </span>
        </div>
        
        {/* 评分标签 */}
        {rating > 0 && (
          <div className="absolute bottom-3 right-3">
            <div className="px-3 py-1.5 bg-black/60 backdrop-blur-md rounded-full flex items-center gap-2 shadow-xl border border-white/10">
              <span className="text-yellow-400 text-lg">⭐</span>
              <span className="text-white text-base font-bold">{displayRating}</span>
            </div>
          </div>
        )}
      </div>
      
      <div className="p-4.5 flex flex-col flex-1 bg-gradient-to-b from-transparent to-black/20">
        <h3 className="text-lg font-black text-white mb-1.5 line-clamp-1 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-pink-400 group-hover:via-purple-400 group-hover:to-cyan-400 transition-all duration-300">
          {anime.title}
        </h3>
        
        {anime.title_jp && (
          <p className="text-xs text-white/50 mb-2 line-clamp-1 font-medium">{anime.title_jp}</p>
        )}
        
        {anime.description && anime.description !== '暂无描述' && (
          <p className="text-sm text-white/70 mb-3.5 line-clamp-2 flex-1 leading-relaxed">
            {anime.description}
          </p>
        )}
        
        <div className="flex items-center justify-between mt-auto pt-3 border-t border-white/10">
          <div className="flex items-center gap-2">
            <StarRating rating={Math.round(rating)} size="sm" readonly />
            {rating > 0 && (
              <span className="text-sm text-white/60 font-bold">
                {displayRating}
              </span>
            )}
          </div>
          
          <div className="flex items-center gap-2.5">
            {anime.studio && anime.studio.trim() !== '' && (
              <span className="text-xs text-white/40 hidden sm:block truncate max-w-[100px]">
                {anime.studio}
              </span>
            )}
            <span className="text-sm text-white/80 font-bold bg-white/10 px-3 py-1 rounded-xl border border-white/10">
              {anime.release_year}
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  const wrapperClass = "anime-card bg-surface border border-white/10 rounded-2xl overflow-hidden transition-all duration-500 hover:border-pink-500/50 hover:shadow-2xl hover:shadow-pink-500/25 hover:-translate-y-3 flex flex-col h-full group";

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
