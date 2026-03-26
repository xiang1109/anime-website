

import { useState } from 'react';

interface StarRatingProps {
  rating: number;
  onRate?: (rating: number) => void;
  size?: 'sm' | 'md' | 'lg';
  readonly?: boolean;
}

const StarRating: React.FC<StarRatingProps> = ({
  rating,
  onRate,
  size = 'md',
  readonly = false
}) => {
  const [hoverRating, setHoverRating] = useState(0);
  
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  };

  const handleStarClick = (starRating: number) => {
    if (!readonly && onRate) {
      onRate(starRating);
    }
  };

  return (
    <div className="star-rating">
      {[1, 2, 3, 4, 5].map((star) => {
        const isFilled = star <= (hoverRating || rating);
        return (
          <svg
            key={star}
            className={`star ${sizeClasses[size]} ${readonly ? 'cursor-default' : 'cursor-pointer'}`}
            fill={isFilled ? '#fbbf24' : 'none'}
            stroke={isFilled ? '#fbbf24' : '#94a3b8'}
            viewBox="0 0 24 24"
            onMouseEnter={() => !readonly && setHoverRating(star)}
            onMouseLeave={() => !readonly && setHoverRating(0)}
            onClick={() => handleStarClick(star)}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
            />
          </svg>
        );
      })}
    </div>
  );
};

export default StarRating;
