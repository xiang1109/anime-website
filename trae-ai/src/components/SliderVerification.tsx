import { useState, useRef, useEffect } from 'react';

interface SliderVerificationProps {
  onVerify: (isVerified: boolean) => void;
}

const SliderVerification: React.FC<SliderVerificationProps> = ({ onVerify }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState(0);
  const [isVerified, setIsVerified] = useState(false);
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
        if (position > 200) {
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
  }, [isDragging, position, onVerify]);

  const resetVerification = () => {
    setIsVerified(false);
    setPosition(0);
    onVerify(false);
  };

  return (
    <div className="w-full">
      <div 
        ref={sliderRef}
        className={`w-full h-10 bg-background border rounded-lg relative cursor-pointer transition-colors ${
          isVerified 
            ? 'border-green-500 bg-green-500/10' 
            : 'border-border hover:border-primary/50'
        }`}
      >
        {!isVerified ? (
          <div 
            ref={handleRef}
            className="absolute left-0 top-0 h-10 w-10 bg-primary text-white rounded-lg flex items-center justify-center transition-transform"
            style={{ transform: `translateX(${position}px)` }}
            onMouseDown={handleMouseDown}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        ) : (
          <div className="absolute left-0 top-0 w-full h-10 flex items-center justify-center">
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
