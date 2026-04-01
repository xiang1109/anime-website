import { useState, useEffect } from 'react';

interface SimpleVerificationProps {
  onVerify: (isVerified: boolean) => void;
}

const SimpleVerification: React.FC<SimpleVerificationProps> = ({ onVerify }) => {
  const [num1, setNum1] = useState(0);
  const [num2, setNum2] = useState(0);
  const [operator, setOperator] = useState<'+' | '-' | '×'>('+');
  const [answer, setAnswer] = useState('');
  const [isVerified, setIsVerified] = useState(false);
  const [error, setError] = useState('');

  // 生成新的数学题
  const generateQuestion = () => {
    const ops: Array<'+' | '-' | '×'> = ['+', '-', '×'];
    const randomOp = ops[Math.floor(Math.random() * ops.length)];
    
    let n1, n2;
    if (randomOp === '+') {
      n1 = Math.floor(Math.random() * 50) + 1;
      n2 = Math.floor(Math.random() * 50) + 1;
    } else if (randomOp === '-') {
      n1 = Math.floor(Math.random() * 50) + 20;
      n2 = Math.floor(Math.random() * 20) + 1;
    } else {
      n1 = Math.floor(Math.random() * 12) + 1;
      n2 = Math.floor(Math.random() * 12) + 1;
    }
    
    setNum1(n1);
    setNum2(n2);
    setOperator(randomOp);
    setAnswer('');
    setError('');
    setIsVerified(false);
    onVerify(false);
  };

  // 计算正确答案
  const getCorrectAnswer = () => {
    switch (operator) {
      case '+': return num1 + num2;
      case '-': return num1 - num2;
      case '×': return num1 * num2;
      default: return 0;
    }
  };

  // 验证答案
  const checkAnswer = () => {
    const userAnswer = parseInt(answer);
    if (isNaN(userAnswer)) {
      setError('请输入数字');
      return;
    }

    if (userAnswer === getCorrectAnswer()) {
      setIsVerified(true);
      setError('');
      onVerify(true);
    } else {
      setError('答案错误，请重试');
      setTimeout(generateQuestion, 1000);
    }
  };

  // 初始化
  useEffect(() => {
    generateQuestion();
  }, []);

  // 重置验证
  const resetVerification = () => {
    generateQuestion();
  };

  // 处理回车键
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !isVerified) {
      checkAnswer();
    }
  };

  return (
    <div className="w-full">
      {/* 验证区域 */}
      <div className="relative w-full p-6 rounded-2xl overflow-hidden border border-white/10 bg-gradient-to-br from-pink-500/10 via-purple-500/10 to-cyan-500/10">
        {/* 装饰元素 */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-3 left-3 w-8 h-8 bg-pink-500/20 rounded-full blur-md animate-pulse" />
          <div className="absolute bottom-3 right-3 w-10 h-10 bg-cyan-500/20 rounded-full blur-md animate-pulse" style={{ animationDelay: '0.5s' }} />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-purple-500/5 rounded-full blur-xl" />
        </div>

        <div className="relative z-10">
          {!isVerified ? (
            <>
              {/* 标题 */}
              <div className="text-center mb-4">
                <div className="text-3xl mb-2">🔢</div>
                <p className="text-white/80 text-sm font-medium">回答数学题完成验证</p>
              </div>

              {/* 数学题 */}
              <div className="flex items-center justify-center gap-4 mb-4">
                <div className="w-16 h-16 bg-white/10 rounded-xl flex items-center justify-center border border-white/20">
                  <span className="text-2xl font-bold text-white">{num1}</span>
                </div>
                <div className="text-2xl font-bold text-pink-400">{operator}</div>
                <div className="w-16 h-16 bg-white/10 rounded-xl flex items-center justify-center border border-white/20">
                  <span className="text-2xl font-bold text-white">{num2}</span>
                </div>
                <div className="text-2xl font-bold text-cyan-400">=</div>
                <div className="w-16 h-16 bg-white/10 rounded-xl flex items-center justify-center border border-white/20">
                  <input
                    type="text"
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value.replace(/\D/g, ''))}
                    onKeyDown={handleKeyDown}
                    className="w-full h-full text-center text-2xl font-bold text-white bg-transparent outline-none"
                    placeholder="?"
                    maxLength={4}
                    autoComplete="off"
                  />
                </div>
              </div>

              {/* 验证按钮 */}
              <button
                onClick={checkAnswer}
                disabled={!answer}
                className="w-full py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-xl font-semibold hover:from-pink-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-purple-500/30"
              >
                验证
              </button>

              {/* 换一题 */}
              <button
                onClick={generateQuestion}
                className="w-full mt-2 py-2 text-white/60 hover:text-white text-sm transition-colors"
              >
                换一题
              </button>

              {/* 错误提示 */}
              {error && (
                <div className="mt-3 text-center">
                  <p className="text-red-400 text-sm">{error}</p>
                </div>
              )}
            </>
          ) : (
            /* 验证成功 */
            <div className="text-center py-4">
              <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg shadow-green-500/30">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-green-400 font-semibold text-lg">验证成功！</p>
              <button
                onClick={resetVerification}
                className="mt-4 text-white/60 hover:text-white text-sm transition-colors flex items-center gap-1.5 mx-auto"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                重新验证
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SimpleVerification;
