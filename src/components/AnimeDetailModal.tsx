import { useState, useEffect } from 'react';
import type { Anime, Comment } from '../types';
import StarRating from './StarRating';
import { useAuth } from '../context/AuthContext';
import API_BASE_URL from '../config/api';

interface AnimeDetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  anime: Anime | null;
}

const AnimeDetailModal: React.FC<AnimeDetailModalProps> = ({ isOpen, onClose, anime }) => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [userRating, setUserRating] = useState<number | null>(null);
  const [averageRating, setAverageRating] = useState(0);
  const [ratingCount, setRatingCount] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingComments, setIsLoadingComments] = useState(false);
  const { token } = useAuth();

  useEffect(() => {
    if (anime && isOpen) {
      setUserRating(null);
      setAverageRating(Number(anime.average_rating || 0));
      setRatingCount(Number(anime.rating_count || 0));
      fetchComments(anime.id);
    }
  }, [anime, isOpen]);

  const fetchComments = async (animeId: number) => {
    if (!animeId) return;
    
    setIsLoadingComments(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/anime/${animeId}/comments`);
      const result = await response.json();
      
      if (response.ok) {
        const data = result.data || result;
        setComments(data.comments || []);
      } else {
        setComments([]);
      }
    } catch (error) {
      console.error('Failed to fetch comments:', error);
      setComments([]);
    } finally {
      setIsLoadingComments(false);
    }
  };

  const handleRate = async (rating: number) => {
    if (!anime || !token) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/anime/${anime.id}/rate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ rating })
      });

      const result = await response.json();
      const data = result.data || result;
      
      if (response.ok) {
        setUserRating(rating);
        setAverageRating(data.average_rating || rating);
        setRatingCount(data.rating_count || (ratingCount + 1));
      } else {
        console.error('Failed to submit rating:', result.message);
      }
    } catch (error) {
      console.error('Failed to submit rating:', error);
    }
  };

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!anime || !token || !newComment.trim()) return;

    setIsSubmitting(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/anime/${anime.id}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: newComment })
      });

      if (response.ok) {
        const result = await response.json();
        const comment = result.data || result;
        setComments([comment, ...comments]);
        setNewComment('');
      } else {
        console.error('Failed to submit comment');
      }
    } catch (error) {
      console.error('Failed to submit comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen || !anime) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-8 pb-8 overflow-y-auto" onClick={onClose}>
      <div className="fixed inset-0 bg-black/70 backdrop-blur-sm" />
      <div
        className="relative bg-surface rounded-xl w-full max-w-4xl mx-4 overflow-hidden border border-border shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="relative">
          <img
            src={anime.cover_image}
            alt={anime.title}
            className="w-full h-auto max-h-[50vh] object-contain"
          />
          <button
            onClick={onClose}
            className="absolute top-4 right-4 bg-background/80 backdrop-blur-sm rounded-full p-2 text-text hover:text-white transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-surface to-transparent h-32" />
        </div>

        <div className="p-6">
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-text mb-2">{anime.title}</h2>
            {anime.title_jp && (
              <p className="text-lg text-text-muted mb-3">{anime.title_jp}</p>
            )}
            <div className="flex items-center gap-4 text-sm text-text-muted mb-4 flex-wrap">
              <span>{anime.studio}</span>
              <span>•</span>
              <span>{anime.release_year}</span>
              <span>•</span>
              <span>{anime.episodes || 12} 集</span>
              <span className="px-2 py-1 bg-primary/20 text-primary rounded-full text-xs">
                {anime.status}
              </span>
              {anime.is_movie && (
                <span className="px-2 py-1 bg-purple-500/20 text-purple-500 rounded-full text-xs">
                  剧场版
                </span>
              )}
              {anime.anime_type && (
                <span className="px-2 py-1 bg-secondary/20 text-secondary rounded-full text-xs">
                  {anime.anime_type}
                </span>
              )}
              {anime.nationality && (
                <span className={`px-2 py-1 text-xs rounded-full ${
                  anime.nationality === '日本' 
                    ? 'bg-red-500/20 text-red-500' 
                    : anime.nationality === '国产' 
                    ? 'bg-green-500/20 text-green-500' 
                    : 'bg-blue-500/20 text-blue-500'
                }`}>
                  {anime.nationality}
                </span>
              )}
            </div>
            <p className="text-text-muted leading-relaxed">{anime.description}</p>
          </div>

          <div className="bg-background rounded-xl p-6 mb-6">
            <h3 className="text-xl font-bold text-text mb-4">评分</h3>
            <div className="flex items-center gap-4">
              <div className="text-4xl font-bold text-text">{averageRating.toFixed(1)}</div>
              <div>
                <StarRating rating={averageRating} size="lg" />
                <p className="text-sm text-text-muted mt-1">{ratingCount} 人评分</p>
              </div>
            </div>
            
            {token && (
              <div className="mt-4 pt-4 border-t border-border">
                <p className="text-sm text-text mb-2">你的评分</p>
                <StarRating
                  rating={userRating || 0}
                  onRate={handleRate}
                  size="lg"
                  interactive={true}
                />
              </div>
            )}
          </div>

          <div className="bg-background rounded-xl p-6 mb-6">
            <h3 className="text-xl font-bold text-text mb-4">评论</h3>
            
            {token && (
              <form onSubmit={handleSubmitComment} className="mb-6">
                <textarea
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="写下你的评论..."
                  className="w-full px-4 py-3 bg-surface border border-border rounded-lg text-text placeholder-text-muted resize-none mb-3"
                  rows={3}
                  disabled={isSubmitting}
                />
                <button
                  type="submit"
                  disabled={isSubmitting || !newComment.trim()}
                  className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? '发布中...' : '发布评论'}
                </button>
              </form>
            )}

            {isLoadingComments ? (
              <div className="text-center py-8">
                <div className="inline-block w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin mb-2" />
                <p className="text-text-muted">加载评论中...</p>
              </div>
            ) : comments.length === 0 ? (
              <div className="text-center py-8 text-text-muted">
                暂无评论，快来抢沙发吧！
              </div>
            ) : (
              <div className="space-y-4">
                {comments.map((comment) => (
                  <div key={comment.id} className="bg-surface rounded-lg p-4">
                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                        <span className="text-primary font-medium">
                          {comment.username?.charAt(0) || '用'}
                        </span>
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-medium text-text">{comment.username || '用户'}</span>
                          <span className="text-xs text-text-muted">
                            {new Date(comment.created_at).toLocaleDateString('zh-CN')}
                          </span>
                        </div>
                        <p className="text-text-muted text-sm">{comment.content}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 雾漫林间介绍 - 放在最底部，字体小一点 */}
          <div className="border-t border-border pt-6">
            <div className="bg-background/50 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                  <svg className="w-3.5 h-3.5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-medium text-text mb-1 text-sm">雾漫林间</h4>
                  <p className="text-xs text-text-muted leading-relaxed">
                    雾漫林间专注于全球高分动漫推荐与评分，为你精选来自世界各地的优质动漫作品。
                    通过我们的平台，你可以发现更多值得一看的好作品，分享你的观影体验，
                    与其他漫迷一起构建专业的动漫推荐社区，探索精彩的动漫世界。
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnimeDetailModal;
