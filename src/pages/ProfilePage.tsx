import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import StarRating from '../components/StarRating';
import API_BASE_URL from '../config/api';

interface UserRating {
  id: number;
  anime_id: number;
  rating: number;
  title: string;
  cover_image: string;
  created_at: string;
}

interface UserComment {
  id: number;
  anime_id: number;
  content: string;
  title: string;
  cover_image: string;
  username: string;
  avatar: string;
  created_at: string;
}

const ProfilePage: React.FC = () => {
  const { user, logout, updateUser } = useAuth();
  const [isUploading, setIsUploading] = useState(false);
  const [ratings, setRatings] = useState<UserRating[]>([]);
  const [comments, setComments] = useState<UserComment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'ratings' | 'comments'>('ratings');

  useEffect(() => {
    if (user) {
      fetchUserData();
    }
  }, [user]);

  const fetchUserData = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      // 获取评分记录
      const ratingsResponse = await fetch(`${API_BASE_URL}/api/user/ratings`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (ratingsResponse.ok) {
        const ratingsResult = await ratingsResponse.json();
        setRatings(ratingsResult.data?.ratings || []);
      }

      // 获取评论记录
      const commentsResponse = await fetch(`${API_BASE_URL}/api/user/comments`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (commentsResponse.ok) {
        const commentsResult = await commentsResponse.json();
        setComments(commentsResult.data?.comments || []);
      }
    } catch (error) {
      console.error('获取用户数据错误:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-text-muted mb-4">请先登录</p>
          <Link
            to="/"
            className="text-primary hover:underline"
          >
            返回首页
          </Link>
        </div>
      </div>
    );
  }

  const handleAvatarUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      alert('请选择图片文件');
      return;
    }

    // 验证文件大小 (最大5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('图片大小不能超过5MB');
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('avatar', file);

      const response = await fetch(`${API_BASE_URL}/api/user/avatar`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        updateUser({ avatar: result.data.avatarUrl });
        alert('头像上传成功！');
      } else {
        alert(result.message || '头像上传失败');
      }
    } catch (error) {
      console.error('上传头像错误:', error);
      alert('头像上传失败，请重试');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 用户信息卡片 */}
        <div className="bg-surface rounded-3xl p-8 border border-white/10 shadow-2xl glass mb-8">
          <div className="flex items-start gap-8">
            <div className="flex-shrink-0 relative group">
              <div className="w-28 h-28 rounded-full overflow-hidden ring-4 ring-pink-500/30 bg-gradient-to-br from-pink-500/20 to-purple-500/20 flex items-center justify-center">
                {user.avatar ? (
                  <img
                    src={user.avatar}
                    alt={user.username}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <span className="text-4xl">👤</span>
                )}
              </div>
              
              {/* 上传按钮 */}
              <label className="absolute bottom-0 right-0 w-10 h-10 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full flex items-center justify-center cursor-pointer hover:scale-110 transition-transform shadow-lg shadow-pink-500/30">
                {isUploading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <span className="text-white text-lg">📷</span>
                )}
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleAvatarUpload}
                  disabled={isUploading}
                  className="hidden"
                />
              </label>
            </div>
            
            <div className="flex-1 pt-2">
              <h1 className="text-3xl font-bold text-white mb-2">{user.username}</h1>
              {user.email && (
                <p className="text-text-muted text-lg mb-6">{user.email}</p>
              )}
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={logout}
                  className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-2xl hover:from-red-600 hover:to-pink-600 transition-all hover:scale-105 shadow-lg shadow-red-500/30"
                >
                  <span>🚪</span>
                  <span>退出登录</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Tab切换 */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setActiveTab('ratings')}
            className={`px-6 py-3 rounded-2xl font-semibold transition-all ${
              activeTab === 'ratings'
                ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-lg shadow-purple-500/30'
                : 'bg-surface text-text-muted hover:text-white border border-white/10'
            }`}
          >
            <span className="mr-2">⭐</span>
            我的评分 ({ratings.length})
          </button>
          <button
            onClick={() => setActiveTab('comments')}
            className={`px-6 py-3 rounded-2xl font-semibold transition-all ${
              activeTab === 'comments'
                ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-lg shadow-purple-500/30'
                : 'bg-surface text-text-muted hover:text-white border border-white/10'
            }`}
          >
            <span className="mr-2">💬</span>
            我的评论 ({comments.length})
          </button>
        </div>

        {/* 评分记录 */}
        {activeTab === 'ratings' && (
          <div className="bg-surface rounded-3xl p-8 border border-white/10 shadow-2xl glass">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <span>⭐</span>
              我的评分
            </h2>
            
            {isLoading ? (
              <div className="text-center py-12">
                <div className="inline-block w-8 h-8 border-4 border-pink-500 border-t-transparent rounded-full animate-spin mb-4" />
                <p className="text-text-muted">加载中...</p>
              </div>
            ) : ratings.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-full flex items-center justify-center">
                  <span className="text-4xl">🎬</span>
                </div>
                <p className="text-text-muted text-lg mb-4">还没有评分记录</p>
                <p className="text-text-muted text-sm mb-6">开始探索动漫，留下你的评价吧！</p>
                <Link
                  to="/"
                  className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-2xl hover:from-pink-600 hover:to-purple-600 transition-all hover:scale-105 shadow-lg shadow-purple-500/30"
                >
                  <span>🔍</span>
                  去发现动漫
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {ratings.map((rating) => (
                  <Link
                    key={rating.id}
                    to={`/anime/${rating.anime_id}`}
                    className="flex items-center gap-4 p-4 bg-background/50 rounded-2xl hover:bg-background/80 transition-colors border border-white/5"
                  >
                    <img
                      src={rating.cover_image}
                      alt={rating.title}
                      className="w-16 h-20 object-cover rounded-lg"
                    />
                    <div className="flex-1">
                      <h3 className="text-white font-semibold mb-2">{rating.title}</h3>
                      <div className="flex items-center gap-3">
                        <StarRating rating={rating.rating} size="md" readonly />
                        <span className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                          {rating.rating}分
                        </span>
                      </div>
                      <p className="text-text-muted text-sm mt-1">
                        {new Date(rating.created_at).toLocaleDateString('zh-CN')}
                      </p>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        )}

        {/* 评论记录 */}
        {activeTab === 'comments' && (
          <div className="bg-surface rounded-3xl p-8 border border-white/10 shadow-2xl glass">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <span>💬</span>
              我的评论
            </h2>
            
            {isLoading ? (
              <div className="text-center py-12">
                <div className="inline-block w-8 h-8 border-4 border-pink-500 border-t-transparent rounded-full animate-spin mb-4" />
                <p className="text-text-muted">加载中...</p>
              </div>
            ) : comments.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-full flex items-center justify-center">
                  <span className="text-4xl">✍️</span>
                </div>
                <p className="text-text-muted text-lg mb-4">还没有评论记录</p>
                <p className="text-text-muted text-sm mb-6">写下你的观影感受吧！</p>
                <Link
                  to="/"
                  className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-2xl hover:from-pink-600 hover:to-purple-600 transition-all hover:scale-105 shadow-lg shadow-purple-500/30"
                >
                  <span>🔍</span>
                  去发现动漫
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {comments.map((comment) => (
                  <Link
                    key={comment.id}
                    to={`/anime/${comment.anime_id}`}
                    className="p-4 bg-background/50 rounded-2xl hover:bg-background/80 transition-colors border border-white/5"
                  >
                    <div className="flex items-start gap-4">
                      <img
                        src={comment.cover_image}
                        alt={comment.title}
                        className="w-16 h-20 object-cover rounded-lg flex-shrink-0"
                      />
                      <div className="flex-1">
                        <h3 className="text-white font-semibold mb-2">{comment.title}</h3>
                        <p className="text-text-muted text-sm mb-2">{comment.content}</p>
                        <p className="text-text-muted text-xs">
                          {new Date(comment.created_at).toLocaleDateString('zh-CN')}
                        </p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default ProfilePage;
