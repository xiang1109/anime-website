import { useState, useEffect } from 'react';

interface HoverStarEffectProps {
  isHovered: boolean;
}

const HoverStarEffect: React.FC<HoverStarEffectProps> = ({ isHovered }) => {
  const [stars, setStars] = useState<{ id: number; x: number; y: number; delay: number; size: number }[]>([]);

  useEffect(() => {
    if (isHovered) {
      const newStars = Array.from({ length: 15 }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        delay: Math.random() * 2,
        size: 2 + Math.random() * 4,
      }));
      setStars(newStars);
    } else {
      setStars([]);
    }
  }, [isHovered]);

  return (
    <div className={`absolute inset-0 overflow-hidden pointer-events-none transition-opacity duration-300 ${isHovered ? 'opacity-100' : 'opacity-0'}`}>
      {stars.map((star) => (
        <div
          key={star.id}
          className="hover-star absolute"
          style={{
            left: `${star.x}%`,
            top: `${star.y}%`,
            width: `${star.size}px`,
            height: `${star.size}px`,
            animationDelay: `${star.delay}s`,
          }}
        />
      ))}
    </div>
  );
};

export default HoverStarEffect;
