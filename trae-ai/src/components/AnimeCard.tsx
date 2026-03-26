import type { Anime } from '../types';
import StarRating from './StarRating';

interface AnimeCardProps {
  anime: Anime;
  onClick: () => void;
}

const AnimeCard: React.FC<AnimeCardProps> = ({ anime, onClick }) => {
  return (
    <div
      className="anime-card bg-surface rounded-xl overflow-hidden cursor-pointer border border-border"
      onClick={onClick}
    >
      <div className="relative">
        <img
          src={anime.cover_image}
          alt={anime.title}
          className="w-full h-64 object-cover"
        />
        <div className="absolute top-3 right-3 bg-background/80 backdrop-blur-sm px-2 py-1 rounded-lg">
          <span className="text-sm font-medium text-text">{anime.status}</span>
        </div>
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold text-text mb-2 line-clamp-1">
          {anime.title}
        </h3>
        <p className="text-sm text-text-muted mb-3 line-clamp-2">
          {anime.description}
        </p>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <StarRating rating={Math.round(Number(anime.average_rating))} size="sm" readonly />
            <span className="text-sm text-text-muted">
              {Number(anime.average_rating) > 0 ? Number(anime.average_rating).toFixed(1) : 'N/A'}
            </span>
          </div>
          <span className="text-xs text-text-muted">
            {anime.rating_count} 评价
          </span>
        </div>
        <div className="mt-3 pt-3 border-t border-border">
          <div className="flex items-center justify-between text-xs text-text-muted">
            <span>{anime.studio}</span>
            <span>{anime.release_year}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnimeCard;
