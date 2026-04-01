import { useState, useRef, useEffect, useCallback } from 'react';

interface SliderVerificationProps {
  onVerify: (isVerified: boolean) => void;
}

const SliderVerification: React.FC<SliderVerificationProps> = ({ onVerify }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState(0);
  const [isVerified, setIsVerified] = useState(false);
  const [targetPosition, setTargetPosition] = useState(200);
  const [sliderWidth, setSliderWidth] = useState(0);
  const sliderRef = useRef<HTMLDivElement>(null);
  const handleRef = useRef<HTMLDivElement>(null);

  // 初始化滑块宽度
  useEffect(() => {
    if (sliderRef.current) {
      setSliderWidth(sliderRef.current.offsetWidth);
      // 设置目标位置在滑块的60%-80%之间
      const minTarget = sliderRef.current.offsetWidth * 0.5;
      const maxTarget = sliderRef.current.offsetWidth * 0.75;
      setTargetPosition(minTarget + Math.random() * (maxTarget - minTarget));
    }
  }, []);

  // 计算最大可拖动距离
  const maxPosition = sliderWidth - 60; // 60px是滑块宽度

  // 鼠标/触摸开始
  const handleStart = useCallback((clientX: number) => {
    if (isVerified) return;
    setIsDragging(true);
  }, [isVerified]);

  // 鼠标/触摸移动
  const handleMove = useCallback((clientX: number) => {
    if (!isDragging || !sliderRef.current) return;

    const sliderRect = sliderRef.current.getBoundingClientRect();
    let newPosition = clientX - sliderRect.left - 30; // 30px是滑块中心偏移
    newPosition = Math.max(0, Math.min(newPosition, maxPosition));
    setPosition(newPosition);
  }, [isDragging, maxPosition]);

  // 鼠标/触摸结束
  const handleEnd = useCallback(() => {
    if (isDragging) {
      setIsDragging(false);
      
      // 验证位置是否在目标位置附近（±15px误差）
      const tolerance = 15;
      if (Math.abs(position - (targetPosition - 30)) < tolerance) {
        setIsVerified(true);
        onVerify(true);
      } else {
        // 验证失败，回弹到起始位置
        setPosition(0);
      }
    }
  }, [isDragging, position, targetPosition, onVerify]);

  // 鼠标事件
  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    handleStart(e.clientX);
  };

  // 触摸事件
  const handleTouchStart = (e: React.TouchEvent) => {
    e.preventDefault();
    handleStart(e.touches[0].clientX);
  };

  // 全局鼠标/触摸事件监听
  useEffect(() => {
    const handleGlobalMouseMove = (e: MouseEvent) => {
      handleMove(e.clientX);
    };

    const handleGlobalTouchMove = (e: TouchEvent) => {
      handleMove(e.touches[0].clientX);
    };

    const handleGlobalMouseUp = () => {
      handleEnd();
    };

    const handleGlobalTouchEnd = () => {
      handleEnd();
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleGlobalMouseMove);
      document.addEventListener('mouseup', handleGlobalMouseUp);
      document.addEventListener('touchmove', handleGlobalTouchMove, { passive: false });
      document.addEventListener('touchend', handleGlobalTouchEnd);
    }

    return () => {
      document.removeEventListener('mousemove', handleGlobalMouseMove);
      document.removeEventListener('mouseup', handleGlobalMouseUp);
      document.removeEventListener('touchmove', handleGlobalTouchMove);
      document.removeEventListener('touchend', handleGlobalTouchEnd);
    };
  }, [isDragging, handleMove, handleEnd]);

  // 重置验证
  const resetVerification = () => {
    setIsVerified(false);
    setPosition(0);
    if (sliderRef.current) {
      const minTarget = sliderRef.current.offsetWidth * 0.5;
      const maxTarget = sliderRef.current.offsetWidth * 0.75;
      setTargetPosition(minTarget + Math.random() * (maxTarget - minTarget));
    }
    onVerify(false);
  };

  return (
    <div className="w-full">
      {/* 验证提示区域 */}
      <div className="relative w-full h-32 mb-4 rounded-2xl overflow-hidden border border-white/10 bg-gradient-to-br from-pink-500/10 via-purple-500/10 to-cyan-500/10">
        {/* 背景装饰 */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-4 left-4 w-16 h-16 bg-pink-500/20 rounded-full blur-xl" />
          <div className="absolute bottom-4 right-4 w-20 h-20 bg-cyan-500/20 rounded-full blur-xl" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-purple-500/10 rounded-full blur-2xl" />
        </div>

        {/* 验证状态显示 */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          {!isVerified ? (
            <>
              <div className="text-4xl mb-2">🎯</div>
              <p className="text-white/70 text-sm font-medium">向右拖动滑块完成验证</p>
              <p className="text-white/40 text-xs mt-1">将滑块移动到目标位置</p>
            </>
          ) : (
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center mb-2 shadow-lg shadow-green-500/30">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-green-400 font-semibold">验证成功！</p>
            </div>
          )}
        </div>

        {/* 目标位置指示器（未验证时显示） */}
        {!isVerified && (
          <div 
            className="absolute top-1/2 -translate-y-1/2 w-14 h-14 rounded-xl border-2 border-dashed border-white/30 bg-white/5"
            style={{ left: `${targetPosition - 28}px` }}
          >
            <div className="absolute inset-2 rounded-lg border border-white/20 animate-pulse" />
          </div>
        )}
      </div>

      {/* 滑块轨道 */}
      <div 
        ref={sliderRef}
        className={`w-full h-14 rounded-2xl relative select-none transition-all ${
          isVerified 
            ? 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/40' 
            : 'bg-white/5 border border-white/10'
        }`}
      >
        {/* 进度填充 */}
        {!isVerified && (
          <div 
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-pink-500/30 via-purple-500/30 to-cyan-500/30 rounded-2xl transition-all"
            style={{ width: `${position + 30}px` }}
          />
        )}

        {/* 提示文字 */}
        {!isVerified && position === 0 && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <span className="text-white/50 text-sm font-medium">按住滑块向右拖动</span>
          </div>
        )}

        {/* 滑块按钮 */}
        {!isVerified ? (
          <div 
            ref={handleRef}
            className="absolute top-1 left-1 h-12 w-12 bg-gradient-to-br from-pink-500 to-purple-500 rounded-xl shadow-lg shadow-purple-500/30 flex items-center justify-center cursor-grab active:cursor-grabbing transition-transform hover:scale-105 select-none z-10"
            style={{ left: `${position}px` }}
            onMouseDown={handleMouseDown}
            onTouchStart={handleTouchStart}
          >
            <div className="relative">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              </svg>
              <div className="absolute inset-0 bg-white/20 rounded-full blur-md" />
            </div>
          </div>
        ) : null}
      </div>
      
      {/* 重新验证按钮 */}
      {isVerified && (
        <button 
          onClick={resetVerification}
          className="mt-4 text-xs text-white/60 hover:text-white transition-colors flex items-center gap-1.5 mx-auto px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          重新验证
        </button>
      )}
    </div>
  );
};

export default SliderVerification;
