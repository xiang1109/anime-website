import { useState, useEffect } from 'react';
import type { Anime, Comment } from '../types';
import StarRating from './StarRating';
import { useAuth } from '../context/AuthContext';

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
  const { user, token } = useAuth();

  useEffect(() => {
    if (anime && isOpen) {
      fetchComments();
      fetchUserRating();
      setAverageRating(Number(anime.average_rating));
      setRatingCount(anime.rating_count);
    }
  }, [anime, isOpen]);

  const fetchComments = async () => {
    if (!anime) return;
    try {
      const response = await fetch(`/api/anime/${anime.id}/comments`);
      const result = await response.json();
      const data = result.data || result;
      setComments(data.comments || data);
    } catch (error) {
      console.error('Failed to fetch comments:', error);
    }
  };

  const fetchUserRating = async () => {
    if (!anime || !token) return;
    try {
      const response = await fetch(`/api/anime/${anime.id}/user-rating`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const result = await response.json();
      const data = result.data || result;
      setUserRating(data.rating);
    } catch (error) {
      console.error('Failed to fetch user rating:', error);
    }
  };

  const handleRate = async (rating: number) => {
    if (!anime || !token) return;
    
    try {
      const response = await fetch(`/api/anime/${anime.id}/rate`, {
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
        setAverageRating(data.average_rating);
        setRatingCount(data.rating_count);
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
      const response = await fetch(`/api/anime/${anime.id}/comments`, {
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
      }
    } catch (error) {
      console.error('Failed to submit comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen || !anime) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-content bg-surface rounded-xl w-full max-w-4xl mx-4 max-h-[90vh] overflow-hidden border border-border"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="relative">
          <img
            src={anime.cover_image}
            alt={anime.title}
            className="w-full h-64 object-cover"
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

        <div className="p-6 overflow-y-auto" style={{ maxHeight: 'calc(90vh - 256px)' }}>
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-text mb-2">{anime.title}</h2>
            <div className="flex items-center gap-4 text-sm text-text-muted mb-4">
              <span>{anime.studio}</span>
              <span>•</span>
              <span>{anime.release_year}</span>
              <span>•</span>
              <span>{anime.episodes} 集</span>
              <span className="px-2 py-1 bg-primary/20 text-primary rounded-full text-xs">
                {anime.status}
              </span>
            </div>
            <p className="text-text-muted leading-relaxed">{anime.description}</p>
          </div>

          <div className="bg-background rounded-xl p-6 mb-6">
            <h3 className="text-xl font-semibold text-text mb-4">评分</h3>
            <div className="flex items-center gap-8">
              <div className="text-center">
                <div className="text-5xl font-bold text-primary mb-2">
                  {averageRating > 0 ? averageRating.toFixed(1) : 'N/A'}
                </div>
                <div className="flex items-center justify-center mb-1">
                  <StarRating rating={Math.round(averageRating)} size="md" readonly />
                </div>
                <span className="text-sm text-text-muted">{ratingCount} 人评价</span>
              </div>
              <div className="flex-1">
                {user ? (
                  <div>
                    <p className="text-text-muted mb-2">你的评分：</p>
                    <StarRating
                      rating={userRating || 0}
                      onRate={handleRate}
                      size="lg"
                    />
                    {userRating && (
                      <p className="text-sm text-success mt-2">
                        你已评分：{userRating} 星
                      </p>
                    )}
                  </div>
                ) : (
                  <p className="text-text-muted">请登录后评分</p>
                )}
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-text mb-4">评论 ({comments.length})</h3>
            
            {user && (
              <form onSubmit={handleSubmitComment} className="mb-6">
                <textarea
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="写下你的评论..."
                  className="w-full px-4 py-3 bg-background border border-border rounded-lg text-text placeholder-text-muted resize-none mb-3"
                  rows={3}
                  required
                />
                <div className="flex justify-end">
                  <button
                    type="submit"
                    disabled={isSubmitting || !newComment.trim()}
                    className="btn-primary px-6 py-2 text-white rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isSubmitting ? '发布中...' : '发布评论'}
                  </button>
                </div>
              </form>
            )}

            <div className="space-y-4">
              {comments.length === 0 ? (
                <p className="text-center text-text-muted py-8">暂无评论，来发表第一条评论吧！</p>
              ) : (
                comments.map((comment) => (
                  <div
                    key={comment.id}
                    className="comment-enter bg-background rounded-lg p-4"
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
                        <span className="text-white font-medium">
                          {comment.username.charAt(0).toUpperCase()}
                        </span>
                      </div>
                      <div>
                        <p className="font-medium text-text">{comment.username}</p>
                        <p className="text-xs text-text-muted">
                          {new Date(comment.created_at).toLocaleString('zh-CN')}
                        </p>
                      </div>
                    </div>
                    <p className="text-text-muted ml-13">{comment.content}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnimeDetailModal;
