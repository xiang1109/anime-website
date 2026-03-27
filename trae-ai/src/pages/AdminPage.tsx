import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface Anime {
  id: number;
  title: string;
  title_jp: string;
  description: string;
  cover_image: string;
  episodes: number;
  status: string;
  release_year: number;
  studio: string;
  genre: string;
  average_rating: number;
  rating_count: number;
  created_at: string;
}

const AdminPage: React.FC = () => {
  const { user, token, isAdmin, isLoading } = useAuth();
  const navigate = useNavigate();
  const [animes, setAnimes] = useState<Anime[]>([]);
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  const [keyword, setKeyword] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingAnime, setEditingAnime] = useState<Anime | null>(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // 表单数据
  const [formData, setFormData] = useState({
    title: '',
    title_jp: '',
    description: '',
    cover_image: '',
    episodes: 0,
    status: '已完结',
    release_year: 2024,
    studio: '',
    genre: '',
    average_rating: 0,
    rating_count: 0
  });

  // 检查管理员权限
  useEffect(() => {
    if (!isLoading && (!user || !isAdmin)) {
      navigate('/');
    }
  }, [user, isAdmin, isLoading, navigate]);

  // 获取动漫列表
  const fetchAnimes = async (page: number = 1, searchKeyword: string = '') => {
    if (!token) return;
    
    setIsLoadingData(true);
    try {
      let url = `/api/admin/animes?page=${page}&limit=10`;
      if (searchKeyword) {
        url += `&keyword=${encodeURIComponent(searchKeyword)}`;
      }

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '获取动漫列表失败');
      }

      const data = result.data || result;
      setAnimes(data.animes || []);
      setTotalPages(data.pagination?.totalPages || 1);
      setTotalResults(data.pagination?.total || 0);
      setCurrentPage(page);
    } catch (err: any) {
      setError(err.message || '获取动漫列表失败');
    } finally {
      setIsLoadingData(false);
    }
  };

  useEffect(() => {
    if (token && isAdmin) {
      fetchAnimes(1, keyword);
    }
  }, [token, isAdmin]);

  // 搜索
  const handleSearch = () => {
    fetchAnimes(1, keyword);
  };

  // 重置表单
  const resetForm = () => {
    setFormData({
      title: '',
      title_jp: '',
      description: '',
      cover_image: '',
      episodes: 0,
      status: '已完结',
      release_year: 2024,
      studio: '',
      genre: '',
      average_rating: 0,
      rating_count: 0
    });
    setEditingAnime(null);
    setShowForm(false);
    setError('');
    setSuccess('');
  };

  // 打开添加表单
  const handleAdd = () => {
    resetForm();
    setShowForm(true);
  };

  // 打开编辑表单
  const handleEdit = (anime: Anime) => {
    setFormData({
      title: anime.title,
      title_jp: anime.title_jp,
      description: anime.description,
      cover_image: anime.cover_image,
      episodes: anime.episodes,
      status: anime.status,
      release_year: anime.release_year,
      studio: anime.studio,
      genre: anime.genre,
      average_rating: anime.average_rating,
      rating_count: anime.rating_count
    });
    setEditingAnime(anime);
    setShowForm(true);
  };

  // 提交表单
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!formData.title.trim()) {
      setError('动漫标题不能为空');
      return;
    }

    try {
      const url = editingAnime
        ? `/api/admin/animes/${editingAnime.id}`
        : '/api/admin/animes';

      const method = editingAnime ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || (editingAnime ? '更新失败' : '添加失败'));
      }

      setSuccess(result.message || (editingAnime ? '更新成功' : '添加成功'));
      
      // 刷新列表
      fetchAnimes(currentPage, keyword);
      
      // 2秒后关闭表单
      setTimeout(() => {
        resetForm();
      }, 1500);
    } catch (err: any) {
      setError(err.message || (editingAnime ? '更新失败' : '添加失败'));
    }
  };

  // 删除动漫
  const handleDelete = async (anime: Anime) => {
    if (!window.confirm(`确定要删除动漫「${anime.title}」吗？\n这将同时删除相关的评分和评论。`)) {
      return;
    }

    try {
      const response = await fetch(`/api/admin/animes/${anime.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || '删除失败');
      }

      setSuccess(result.message || '删除成功');
      
      // 刷新列表
      fetchAnimes(currentPage, keyword);
      
      setTimeout(() => setSuccess(''), 3000);
    } catch (err: any) {
      setError(err.message || '删除失败');
      setTimeout(() => setError(''), 3000);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-text">加载中...</div>
      </div>
    );
  }

  if (!user || !isAdmin) {
    return null; // 会被重定向
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar
        onLoginClick={() => {}}
        onRegisterClick={() => {}}
        showHome={true}
        onHomeClick={() => navigate('/')}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 页面标题 */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-text mb-2">管理员后台</h1>
            <p className="text-text-muted">管理动漫数据库，进行增删改查操作</p>
          </div>
          <button
            onClick={handleAdd}
            className="btn-primary px-6 py-2 text-white rounded-lg font-medium flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            添加动漫
          </button>
        </div>

        {/* 消息提示 */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}
        {success && (
          <div className="bg-green-500/10 border border-green-500/50 text-green-400 px-4 py-3 rounded-lg mb-6">
            {success}
          </div>
        )}

        {/* 搜索栏 */}
        <div className="bg-surface border border-border rounded-xl p-4 mb-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="搜索动漫标题、工作室..."
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text placeholder-text-muted"
              />
            </div>
            <button
              onClick={handleSearch}
              className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
            >
              搜索
            </button>
          </div>
        </div>

        {/* 添加/编辑表单 */}
        {showForm && (
          <div className="bg-surface border border-border rounded-xl p-6 mb-6">
            <h2 className="text-xl font-bold text-text mb-6">
              {editingAnime ? '编辑动漫' : '添加新动漫'}
            </h2>
            
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text mb-2">中文标题 *</label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    placeholder="请输入中文标题"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">日文标题</label>
                  <input
                    type="text"
                    value={formData.title_jp}
                    onChange={(e) => setFormData({ ...formData, title_jp: e.target.value })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    placeholder="请输入日文标题（可选）"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">封面图片URL</label>
                  <input
                    type="url"
                    value={formData.cover_image}
                    onChange={(e) => setFormData({ ...formData, cover_image: e.target.value })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    placeholder="https://..."
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">工作室</label>
                  <input
                    type="text"
                    value={formData.studio}
                    onChange={(e) => setFormData({ ...formData, studio: e.target.value })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    placeholder="制作公司"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">类型</label>
                  <input
                    type="text"
                    value={formData.genre}
                    onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    placeholder="动作,冒险,奇幻"
                  />
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text mb-2">集数</label>
                  <input
                    type="number"
                    value={formData.episodes}
                    onChange={(e) => setFormData({ ...formData, episodes: parseInt(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    min="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">状态</label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                  >
                    <option value="未播出">未播出</option>
                    <option value="连载中">连载中</option>
                    <option value="已完结">已完结</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">年份</label>
                  <input
                    type="number"
                    value={formData.release_year}
                    onChange={(e) => setFormData({ ...formData, release_year: parseInt(e.target.value) || 2024 })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    min="1990"
                    max="2030"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">评分（0-5）</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.average_rating}
                    onChange={(e) => setFormData({ ...formData, average_rating: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    min="0"
                    max="5"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">评分人数</label>
                  <input
                    type="number"
                    value={formData.rating_count}
                    onChange={(e) => setFormData({ ...formData, rating_count: parseInt(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text"
                    min="0"
                  />
                </div>
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-text mb-2">简介</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-4 py-2 bg-background border border-border rounded-lg text-text resize-none"
                  rows={4}
                  placeholder="动漫简介..."
                />
              </div>

              <div className="md:col-span-2 flex gap-4">
                <button
                  type="submit"
                  className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
                >
                  {editingAnime ? '保存修改' : '添加动漫'}
                </button>
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-6 py-2 bg-surface border border-border text-text rounded-lg hover:bg-surface/80 transition-colors"
                >
                  取消
                </button>
              </div>
            </form>
          </div>
        )}

        {/* 动漫列表 */}
        <div className="bg-surface border border-border rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-background">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider">ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider">封面</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider">标题</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider">年份</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider">状态</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider">评分</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {isLoadingData ? (
                  <tr>
                    <td colSpan={7} className="px-4 py-8 text-center text-text-muted">
                      加载中...
                    </td>
                  </tr>
                ) : animes.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-4 py-8 text-center text-text-muted">
                      暂无动漫数据
                    </td>
                  </tr>
                ) : (
                  animes.map((anime) => (
                    <tr key={anime.id} className="hover:bg-background/50 transition-colors">
                      <td className="px-4 py-3 text-sm text-text">{anime.id}</td>
                      <td className="px-4 py-3">
                        <img
                          src={anime.cover_image || 'https://picsum.photos/seed/default/60/80'}
                          alt={anime.title}
                          className="w-12 h-16 object-cover rounded"
                        />
                      </td>
                      <td className="px-4 py-3">
                        <div className="text-sm font-medium text-text">{anime.title}</div>
                        <div className="text-xs text-text-muted">{anime.studio}</div>
                      </td>
                      <td className="px-4 py-3 text-sm text-text">{anime.release_year || '-'}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          anime.status === '连载中' 
                            ? 'bg-green-500/20 text-green-400' 
                            : 'bg-gray-500/20 text-gray-400'
                        }`}>
                          {anime.status}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <div className="text-sm font-medium text-text">{anime.average_rating}</div>
                        <div className="text-xs text-text-muted">{anime.rating_count}人</div>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleEdit(anime)}
                            className="px-3 py-1 text-xs bg-blue-500/20 text-blue-400 rounded hover:bg-blue-500/30 transition-colors"
                          >
                            编辑
                          </button>
                          <button
                            onClick={() => handleDelete(anime)}
                            className="px-3 py-1 text-xs bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 transition-colors"
                          >
                            删除
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* 分页 */}
          {totalPages > 1 && (
            <div className="px-4 py-4 border-t border-border flex items-center justify-between">
              <div className="text-sm text-text-muted">
                共 {totalResults} 条记录，第 {currentPage} / {totalPages} 页
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => fetchAnimes(currentPage - 1, keyword)}
                  disabled={currentPage === 1}
                  className="px-3 py-1 text-sm bg-surface border border-border rounded text-text disabled:opacity-50 disabled:cursor-not-allowed hover:border-primary/50 transition-colors"
                >
                  上一页
                </button>
                <button
                  onClick={() => fetchAnimes(currentPage + 1, keyword)}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 text-sm bg-surface border border-border rounded text-text disabled:opacity-50 disabled:cursor-not-allowed hover:border-primary/50 transition-colors"
                >
                  下一页
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default AdminPage;
