import type { Anime } from '../types';
import StarRating from './StarRating';

interface AnimeCardProps {
  anime: Anime;
  onClick: () => void;
}

const AnimeCard: React.FC<AnimeCardProps> = ({ anime, onClick }) => {
  return (
    <div
      className="anime-card bg-surface border border-border rounded-xl overflow-hidden cursor-pointer hover:border-primary transition-all duration-300"
      onClick={onClick}
    >
      <div className="relative">
        <img
          src={anime.cover_image}
          alt={anime.title}
          className="w-full h-64 object-cover"
        />
        <div className="absolute top-2 left-2 flex gap-2 flex-wrap">
          {anime.nationality && anime.nationality !== '日本' && (
            <span className={`px-2 py-1 text-xs rounded-full ${
              anime.nationality === '国产' 
                ? 'bg-green-500/80 text-white' 
                : 'bg-blue-500/80 text-white'
            }`}>
              {anime.nationality}
            </span>
          )}
          {anime.is_movie && (
            <span className="px-2 py-1 text-xs rounded-full bg-purple-500/80 text-white">
              剧场版
            </span>
          )}
          {anime.anime_type && (
            <span className={`px-2 py-1 text-xs rounded-full ${
              anime.anime_type === '热血' 
                ? 'bg-red-500/80 text-white' 
                : anime.anime_type === '冒险' 
                ? 'bg-blue-500/80 text-white' 
                : anime.anime_type === '喜剧' 
                ? 'bg-yellow-500/80 text-white' 
                : anime.anime_type === '科幻' 
                ? 'bg-cyan-500/80 text-white' 
                : anime.anime_type === '悬疑' 
                ? 'bg-gray-500/80 text-white' 
                : anime.anime_type === '治愈' 
                ? 'bg-pink-500/80 text-white' 
                : anime.anime_type === '运动' 
                ? 'bg-orange-500/80 text-white' 
                : 'bg-gray-500/80 text-white'
            }`}>
              {anime.anime_type}
            </span>
          )}
        </div>
        <div className="absolute top-2 right-2">
          <span className={`px-2 py-1 text-xs rounded-full ${
            anime.status === '连载中' 
              ? 'bg-green-500/80 text-white' 
              : 'bg-gray-500/80 text-white'
          }`}>
            {anime.status}
          </span>
        </div>
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold text-text mb-2 line-clamp-1">{anime.title}</h3>
        {anime.title_jp && (
          <p className="text-xs text-text-muted mb-2 line-clamp-1">{anime.title_jp}</p>
        )}
        <p className="text-sm text-text-muted mb-3 line-clamp-2">{anime.description}</p>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <StarRating rating={Math.round(Number(anime.average_rating))} size="sm" readonly />
            <span className="text-sm text-text-muted">
              {Number(anime.average_rating) > 0 ? Number(anime.average_rating).toFixed(1) : 'N/A'}
            </span>
          </div>
          <span className="text-sm text-text-muted">{anime.release_year}</span>
        </div>
      </div>
    </div>
  );
};

export default AnimeCard;
