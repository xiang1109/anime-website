import { useState, useRef, useEffect } from 'react';

interface SliderVerificationProps {
  onVerify: (isVerified: boolean) => void;
}

const SliderVerification: React.FC<SliderVerificationProps> = ({ onVerify }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState(0);
  const [isVerified, setIsVerified] = useState(false);
  const [targetPosition, setTargetPosition] = useState(Math.random() * 200 + 50);
  const sliderRef = useRef<HTMLDivElement>(null);
  const handleRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = (_e: React.MouseEvent<HTMLDivElement>) => {
    setIsDragging(true);
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging || !sliderRef.current || !handleRef.current) return;

      const sliderRect = sliderRef.current.getBoundingClientRect();
      let newPosition = e.clientX - sliderRect.left;
      newPosition = Math.max(0, Math.min(newPosition, sliderRect.width - 40));
      setPosition(newPosition);
    };

    const handleMouseUp = () => {
      if (isDragging) {
        setIsDragging(false);
        // 验证位置是否在目标位置附近
        if (Math.abs(position - targetPosition) < 10) {
          setIsVerified(true);
          onVerify(true);
        } else {
          setPosition(0);
        }
      }
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, position, targetPosition, onVerify]);

  const resetVerification = () => {
    setIsVerified(false);
    setPosition(0);
    setTargetPosition(Math.random() * 200 + 50);
    onVerify(false);
  };

  return (
    <div className="w-full">
      {/* 拼图验证区域 */}
      <div className="relative w-full h-52 mb-4 rounded-2xl overflow-hidden border border-white/10">
        <div className="w-full h-full">
          <img 
            src="https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=600&q=80" 
            alt="验证背景" 
            className="w-full h-full object-cover"
          />
          {/* 渐变叠加层 */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
          
          {/* 拼图缺口 */}
          {!isVerified && (
            <div 
              className="absolute top-16 w-14 h-14 rounded-xl bg-white/20 backdrop-blur-sm border-2 border-white/40"
              style={{ left: `${targetPosition}px` }}
            >
              <div className="absolute inset-2 rounded-lg bg-white/10 animate-pulse" />
            </div>
          )}
        </div>
      </div>

      {/* 滑块区域 */}
      <div 
        ref={sliderRef}
        className={`w-full h-14 rounded-2xl relative cursor-pointer transition-all overflow-hidden ${
          isVerified 
            ? 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/40' 
            : 'bg-white/5 border border-white/10 hover:border-white/20'
        }`}
      >
        {/* 背景进度条 */}
        {!isVerified && (
          <div 
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-pink-500/20 to-purple-500/20 transition-all"
            style={{ width: `${position}px` }}
          />
        )}
        
        {/* 滑块提示文字 */}
        {!isVerified && position === 0 && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-white/40 text-sm font-medium">按住滑块向右拖动完成验证</span>
          </div>
        )}

        {!isVerified ? (
          <div 
            ref={handleRef}
            className="absolute left-1 top-1 h-12 w-12 bg-gradient-to-br from-pink-500 to-purple-500 rounded-xl shadow-lg shadow-pink-500/30 flex items-center justify-center transition-transform hover:scale-105"
            style={{ transform: `translateX(${position}px)` }}
            onMouseDown={handleMouseDown}
          >
            <div className="relative">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              </svg>
              {/* 装饰性光晕 */}
              <div className="absolute inset-0 bg-white/20 rounded-full blur-md" />
            </div>
          </div>
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-green-400 font-semibold">验证成功</span>
            </div>
          </div>
        )}
      </div>
      
      {isVerified && (
        <button 
          onClick={resetVerification}
          className="mt-3 text-xs text-white/50 hover:text-white/80 transition-colors flex items-center gap-1 mx-auto"
        >
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          重新验证
        </button>
      )}
    </div>
  );
};

export default SliderVerification;
