import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import SliderVerification from './SliderVerification';

interface RegisterModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSwitchToLogin: () => void;
}

const RegisterModal: React.FC<RegisterModalProps> = ({ isOpen, onClose, onSwitchToLogin }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [verifyCode, setVerifyCode] = useState('');
  const [sliderToken, setSliderToken] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSendingCode, setIsSendingCode] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const [isSliderVerified, setIsSliderVerified] = useState(false);
  const { login } = useAuth();

  // 获取滑块令牌
  useEffect(() => {
    if (isOpen) {
      fetchSliderToken();
      // 重置状态
      setError('');
      setSuccess(false);
      setIsSliderVerified(false);
      setCountdown(0);
    }
  }, [isOpen]);

  // 倒计时
  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  const fetchSliderToken = async () => {
    try {
      const response = await fetch('/api/slider-token');
      const result = await response.json();
      if (result.success) {
        setSliderToken(result.data.sliderToken);
      }
    } catch (error) {
      console.error('获取滑块令牌失败:', error);
    }
  };

  // 滑块验证回调
  const handleSliderVerify = (isVerified: boolean) => {
    setIsSliderVerified(isVerified);
    if (isVerified) {
      setError('');
    }
  };

  // 发送验证码
  const handleSendCode = async () => {
    if (!email || !/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(email)) {
      setError('请输入正确的邮箱格式');
      return;
    }

    if (!isSliderVerified) {
      setError('请先完成滑块验证');
      return;
    }

    setIsSendingCode(true);
    setError('');

    try {
      const response = await fetch('/api/send-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, sliderToken }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.message || '发送验证码失败');
      }

      // 更新滑块令牌
      if (result.data?.sliderToken) {
        setSliderToken(result.data.sliderToken);
      }

      // 设置倒计时
      setCountdown(60);
      
      // 测试环境下显示验证码
      if (result.data?.testCode) {
        setVerifyCode(result.data.testCode);
        console.log('测试验证码:', result.data.testCode);
      }

    } catch (err: any) {
      setError(err.message || '发送验证码失败，请重试');
    } finally {
      setIsSendingCode(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    // 验证
    if (!username || username.length < 3) {
      setError('用户名至少需要3个字符');
      return;
    }

    if (!email || !/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(email)) {
      setError('请输入正确的邮箱格式');
      return;
    }

    if (!verifyCode || verifyCode.length !== 6) {
      setError('请输入6位验证码');
      return;
    }

    if (password !== confirmPassword) {
      setError('两次输入的密码不一致');
      return;
    }

    if (password.length < 6) {
      setError('密码至少需要6个字符');
      return;
    }

    if (!isSliderVerified) {
      setError('请先完成滑块验证');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username, 
          email, 
          password, 
          verifyCode,
          sliderToken 
        }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.message || '注册失败');
      }

      const data = result.data || result;
      setSuccess(true);
      
      // 自动登录
      if (data.token && data.user) {
        login(data.token, data.user);
      }

      setTimeout(() => {
        onClose();
        // 重置表单
        setUsername('');
        setEmail('');
        setPassword('');
        setConfirmPassword('');
        setVerifyCode('');
      }, 1500);
    } catch (err: any) {
      setError(err.message || '注册失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-content bg-surface rounded-xl p-6 w-full max-w-md mx-4 border border-border max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-text">注册</h2>
          <button
            onClick={onClose}
            className="text-text-muted hover:text-text transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg mb-4 text-sm">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-500/10 border border-green-500/50 text-green-400 px-4 py-3 rounded-lg mb-4 text-sm">
            注册成功！
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              用户名
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 bg-background border border-border rounded-lg text-text placeholder-text-muted"
              placeholder="请输入用户名（至少3个字符）"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">
              邮箱
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-background border border-border rounded-lg text-text placeholder-text-muted"
              placeholder="请输入邮箱地址"
              required
            />
          </div>

          {/* 滑块验证区域 */}
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              滑块验证
            </label>
            <SliderVerification onVerify={handleSliderVerify} />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">
              验证码
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={verifyCode}
                onChange={(e) => setVerifyCode(e.target.value.replace(/\D/g, ''))}
                className="flex-1 px-4 py-3 bg-background border border-border rounded-lg text-text placeholder-text-muted"
                placeholder="请输入6位验证码"
                maxLength={6}
                required
              />
              <button
                type="button"
                onClick={handleSendCode}
                disabled={isSendingCode || countdown > 0 || !isSliderVerified}
                className={`px-4 py-3 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                  isSendingCode || countdown > 0 || !isSliderVerified
                    ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                    : 'bg-primary text-white hover:bg-primary/90'
                }`}
              >
                {countdown > 0 ? `${countdown}s后重发` : '发送验证码'}
              </button>
            </div>
            <p className="text-xs text-text-muted mt-1">测试环境：验证码将自动填入</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">
              密码
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-background border border-border rounded-lg text-text placeholder-text-muted"
              placeholder="请输入密码（至少6个字符）"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">
              确认密码
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-3 bg-background border border-border rounded-lg text-text placeholder-text-muted"
              placeholder="请再次输入密码"
              required
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? '注册中...' : '注册'}
          </button>
        </form>

        <p className="mt-6 text-center text-text-muted">
          已有账号？
          <button
            onClick={onSwitchToLogin}
            className="text-primary hover:text-primary/80 ml-1 font-medium"
          >
            立即登录
          </button>
        </p>
      </div>
    </div>
  );
};

export default RegisterModal;
