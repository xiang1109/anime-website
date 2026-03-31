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
      <div className="relative w-full h-48 mb-4">
        <div className="w-full h-full rounded-lg overflow-hidden">
          <img 
            src="https://img.freepik.com/free-photo/beautiful-mountain-landscape_1208-334.jpg" 
            alt="验证背景" 
            className="w-full h-full object-cover"
          />
          {/* 拼图缺口 */}
          {!isVerified && (
            <div 
              className="absolute left-0 top-12 w-16 h-16 bg-white/30 backdrop-blur-sm"
              style={{ left: `${targetPosition}px` }}
            >
              <div className="w-full h-full border-2 border-white/50 flex items-center justify-center">
                <div className="w-12 h-12 bg-transparent border-2 border-white/70 rounded-sm"></div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 滑块区域 */}
      <div 
        ref={sliderRef}
        className={`w-full h-12 bg-background border rounded-lg relative cursor-pointer transition-colors ${
          isVerified 
            ? 'border-green-500 bg-green-500/10' 
            : 'border-border hover:border-primary/50'
        }`}
      >
        {!isVerified ? (
          <div 
            ref={handleRef}
            className="absolute left-0 top-0 h-12 w-12 bg-white border border-border rounded-lg shadow-md flex items-center justify-center transition-transform"
            style={{ transform: `translateX(${position}px)` }}
            onMouseDown={handleMouseDown}
          >
            <div className="w-8 h-8 bg-primary/10 rounded-sm flex items-center justify-center">
              <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
              </svg>
            </div>
          </div>
        ) : (
          <div className="absolute left-0 top-0 w-full h-12 flex items-center justify-center">
            <svg className="w-5 h-5 text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-green-400 font-medium">验证成功</span>
          </div>
        )}
      </div>
      
      {isVerified && (
        <button 
          onClick={resetVerification}
          className="mt-2 text-xs text-text-muted hover:text-text transition-colors"
        >
          重新验证
        </button>
      )}
    </div>
  );
};

export default SliderVerification;
