import { useEffect, useRef } from 'react';

const SakuraDecoration: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;

    // 创建樱花花瓣
    const createSakuraPetal = () => {
      const petal = document.createElement('div');
      petal.className = 'sakura-petal';
      
      const startX = Math.random() * window.innerWidth;
      const duration = 8 + Math.random() * 8;
      const delay = Math.random() * 5;
      const size = 8 + Math.random() * 10;
      
      petal.style.left = `${startX}px`;
      petal.style.top = '-20px';
      petal.style.width = `${size}px`;
      petal.style.height = `${size}px`;
      petal.style.animationDuration = `${duration}s`;
      petal.style.animationDelay = `${delay}s`;
      
      container.appendChild(petal);
      
      // 动画结束后移除元素
      setTimeout(() => {
        if (petal.parentNode === container) {
          container.removeChild(petal);
        }
      }, (duration + delay) * 1000);
    };

    // 创建星星
    const createStar = () => {
      const star = document.createElement('div');
      star.className = 'star';
      
      const x = Math.random() * window.innerWidth;
      const y = Math.random() * window.innerHeight;
      const delay = Math.random() * 2;
      
      star.style.left = `${x}px`;
      star.style.top = `${y}px`;
      star.style.animationDelay = `${delay}s`;
      
      container.appendChild(star);
    };

    // 创建梦幻光晕
    const createGlow = () => {
      const glow = document.createElement('div');
      glow.className = 'dreamy-glow';
      
      const size = 200 + Math.random() * 300;
      const x = Math.random() * window.innerWidth - size / 2;
      const y = Math.random() * window.innerHeight - size / 2;
      const hue = 300 + Math.random() * 60; // 粉紫色调
      
      glow.style.width = `${size}px`;
      glow.style.height = `${size}px`;
      glow.style.left = `${x}px`;
      glow.style.top = `${y}px`;
      glow.style.background = `radial-gradient(circle, hsla(${hue}, 70%, 60%, 0.3) 0%, transparent 70%)`;
      
      container.appendChild(glow);
    };

    // 初始化星星
    for (let i = 0; i < 30; i++) {
      createStar();
    }

    // 初始化光晕
    for (let i = 0; i < 3; i++) {
      createGlow();
    }

    // 定时创建樱花
    const sakuraInterval = setInterval(createSakuraPetal, 800);

    // 窗口大小变化时重新创建装饰
    const handleResize = () => {
      container.innerHTML = '';
      for (let i = 0; i < 30; i++) {
        createStar();
      }
      for (let i = 0; i < 3; i++) {
        createGlow();
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      clearInterval(sakuraInterval);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return <div ref={containerRef} className="fixed inset-0 overflow-hidden pointer-events-none" />;
};

export default SakuraDecoration;
