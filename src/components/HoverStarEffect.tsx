import { useEffect, useRef, useState } from 'react';

interface HoverStarEffectProps {
  isHovered: boolean;
}

const HoverStarEffect: React.FC<HoverStarEffectProps> = ({ isHovered }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [stars, setStars] = useState<HTMLDivElement[]>([]);

  useEffect(() => {
    if (!containerRef.current || !isHovered) return;

    const container = containerRef.current;
    const newStars: HTMLDivElement[] = [];

    // 创建星星
    for (let i = 0; i < 20; i++) {
      const star = document.createElement('div');
      star.className = 'hover-star';
      
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      const delay = Math.random() * 2;
      const size = 2 + Math.random() * 4;
      
      star.style.left = `${x}%`;
      star.style.top = `${y}%`;
      star.style.animationDelay = `${delay}s`;
      star.style.width = `${size}px`;
      star.style.height = `${size}px`;
      
      container.appendChild(star);
      newStars.push(star);
    }

    setStars(newStars);

    return () => {
      newStars.forEach(star => {
        if (star.parentNode === container) {
          container.removeChild(star);
        }
      });
    };
  }, [isHovered]);

  return (
    <div 
      ref={containerRef} 
      className={`absolute inset-0 overflow-hidden pointer-events-none transition-opacity duration-300 ${isHovered ? 'opacity-100' : 'opacity-0'}`} 
    />
  );
};

export default HoverStarEffect;
