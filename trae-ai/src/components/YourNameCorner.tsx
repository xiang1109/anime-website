import { useState, useEffect } from 'react';

const YourNameCorner: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // 当组件挂载时，设置可见性为true，触发动画
    setIsVisible(true);
  }, []);

  return (
    <div className="fixed bottom-6 right-6 z-20 pointer-events-none">
      <div 
        className={`transition-all duration-1000 ease-out transform ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}
      >
        {/* 秒速五厘米图片 */}
        <div className="relative">
          <div className="w-40 h-60 rounded-xl overflow-hidden shadow-2xl border border-white/20">
            <img 
              src="https://cdn.myanimelist.net/images/anime/11/19844.jpg" 
              alt="秒速五厘米" 
              className="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
            />
          </div>
          
          {/* 台词气泡 */}
          <div className="absolute -top-20 -left-40 bg-surface/90 backdrop-blur-sm border border-white/20 rounded-xl p-4 max-w-xs shadow-xl">
            <p className="text-white text-sm italic">
              "樱花飘落的速度是每秒五厘米，那么我要以怎样的速度，才能与你相遇？"
            </p>
            <p className="text-blue-300 text-xs mt-2 text-right">
              —— 秒速五厘米
            </p>
          </div>
        </div>

        {/* 樱花飘落动画 */}
        <div className="absolute -top-40 -left-40 w-60 h-60 pointer-events-none">
          {[...Array(10)].map((_, i) => (
            <div 
              key={i}
              className="absolute bg-pink-200 rounded-full opacity-70"
              style={{
                width: `${Math.random() * 8 + 4}px`,
                height: `${Math.random() * 8 + 4}px`,
                left: `${Math.random() * 100}%`,
                top: `-20px`,
                animation: `fall ${Math.random() * 8 + 8}s linear ${Math.random() * 4}s infinite`,
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default YourNameCorner;
