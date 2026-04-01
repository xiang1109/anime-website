import { useState } from 'react';

interface StarRatingProps {
  rating: number;
  onRate?: (rating: number) => void;
  size?: 'sm' | 'md' | 'lg';
  readonly?: boolean;
  interactive?: boolean;
}

const StarRating: React.FC<StarRatingProps> = ({
  rating,
  onRate,
  size = 'md',
  readonly = false,
  interactive = false
}) => {
  const [hoverRating, setHoverRating] = useState(0);
  
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  };

  // 评分范围是1-10分，每个星星代表2分，支持半星（1分）
  // 把评分转换成0-5的星星值
  const normalizedRating = rating / 2;
  const normalizedHoverRating = hoverRating / 2;

  const handleStarClick = (starRating: number, isHalf: boolean) => {
    if (!(readonly || !interactive) && onRate) {
      // 计算实际评分：半星是1分，整星是2分
      const actualRating = isHalf ? (starRating - 1) * 2 + 1 : starRating * 2;
      onRate(actualRating);
    }
  };

  const handleStarMouseEnter = (starRating: number, isHalf: boolean) => {
    if (!(readonly || !interactive)) {
      const actualRating = isHalf ? (starRating - 1) * 2 + 1 : starRating * 2;
      setHoverRating(actualRating);
    }
  };

  const handleStarMouseLeave = () => {
    if (!(readonly || !interactive)) {
      setHoverRating(0);
    }
  };

  return (
    <div className="star-rating flex items-center">
      {[1, 2, 3, 4, 5].map((star) => {
        const currentRating = normalizedHoverRating || normalizedRating;
        const isFilled = star <= Math.floor(currentRating);
        const isHalf = !isFilled && star === Math.ceil(currentRating) && currentRating % 1 !== 0;
        
        return (
          <div 
            key={star} 
            className={`relative ${(readonly || !interactive) ? 'cursor-default' : 'cursor-pointer'}`}
            onMouseLeave={handleStarMouseLeave}
          >
            {/* 左半部分 - 半星 */}
            <div
              className="absolute left-0 top-0 w-1/2 h-full z-10"
              onMouseEnter={() => handleStarMouseEnter(star, true)}
              onClick={() => handleStarClick(star, true)}
            />
            
            {/* 右半部分 - 整星 */}
            <div
              className="absolute right-0 top-0 w-1/2 h-full z-10"
              onMouseEnter={() => handleStarMouseEnter(star, false)}
              onClick={() => handleStarClick(star, false)}
            />

            {/* 星星背景 */}
            <svg
              className={`star ${sizeClasses[size]}`}
              fill="none"
              stroke="#94a3b8"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
              />
            </svg>

            {/* 半星填充 */}
            {isHalf && (
              <svg
                className={`star ${sizeClasses[size]} absolute top-0 left-0`}
                style={{ clipPath: 'inset(0 50% 0 0)' }}
                fill="#fbbf24"
                stroke="#fbbf24"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                />
              </svg>
            )}

            {/* 整星填充 */}
            {isFilled && (
              <svg
                className={`star ${sizeClasses[size]} absolute top-0 left-0`}
                fill="#fbbf24"
                stroke="#fbbf24"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                />
              </svg>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default StarRating;
