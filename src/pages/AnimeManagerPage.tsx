import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import API_BASE_URL from '../config/api';

interface Anime {
  id: number;
  title: string;
  title_jp: string | null;
  cover_image: string;
  studio: string | null;
  release_year: number | null;
  rating: number | null;
}

interface BangumiResult {
  id: number;
  title: string;
  title_cn: string;
  cover: string;
  summary: string;
  score: number;
  air_date: string;
}

interface Pagination {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

const AnimeManagerPage = () => {
  const { user } = useAuth();
  const [animes, setAnimes] = useState<Anime[]>([]);
  const [pagination, setPagination] = useState<Pagination>({ page: 1, limit: 20, total: 0, totalPages: 0 });
  const [loading, setLoading] = useState(false);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [selectedAnime, setSelectedAnime] = useState<Anime | null>(null);
  const [editForm, setEditForm] = useState({
    title: '',
    title_jp: '',
    cover_image: '',
    studio: '',
    release_year: '',
    description: '',
    episodes: '',
    status: '',
    genre: '',
    rating: ''
  });
  const [bangumiSearch, setBangumiSearch] = useState('');
  const [bangumiResults, setBangumiResults] = useState<BangumiResult[]>([]);
  const [bangumiLoading, setBangumiLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // 检查是否是管理员
  const isAdmin = user?.username === 'admin';

  // 获取需要修复的动漫列表
  const fetchAnimes = async (page = 1, search = '') => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: '20',
        ...(search && { search })
      });
      
      const response = await fetch(`${API_BASE_URL}/api/admin/anime/needs-fix?${params}`);
      const data = await response.json();
      
      if (data.animes) {
        setAnimes(data.animes);
        setPagination(data.pagination);
      }
    } catch (error) {
      console.error('获取动漫列表失败:', error);
      setMessage({ type: 'error', text: '获取列表失败' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAdmin) {
      fetchAnimes();
    }
  }, [isAdmin]);

  // 搜索Bangumi
  const searchBangumi = async () => {
    if (!bangumiSearch.trim()) return;
    
    setBangumiLoading(true);
    setBangumiResults([]);
    
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/admin/anime/search-bangumi?keyword=${encodeURIComponent(bangumiSearch)}`
      );
      const data = await response.json();
      
      if (data.results) {
        setBangumiResults(data.results);
      }
    } catch (error) {
      console.error('Bangumi搜索失败:', error);
      setMessage({ type: 'error', text: '搜索失败' });
    } finally {
      setBangumiLoading(false);
    }
  };

  // 从Bangumi导入
  const importFromBangumi = async (animeId: number, bangumiId: number) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/admin/anime/import-from-bangumi/${animeId}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ bangumiId })
        }
      );
      
      const data = await response.json();
      
      if (data.success) {
        setMessage({ type: 'success', text: '导入成功！' });
        fetchAnimes(pagination.page, searchKeyword);
        setSelectedAnime(null);
        setBangumiResults([]);
        setBangumiSearch('');
      } else {
        setMessage({ type: 'error', text: data.error || '导入失败' });
      }
    } catch (error) {
      console.error('导入失败:', error);
      setMessage({ type: 'error', text: '导入失败' });
    }
  };

  // 更新动漫信息
  const updateAnime = async () => {
    if (!selectedAnime) return;
    
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/admin/anime/${selectedAnime.id}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...editForm,
            release_year: editForm.release_year ? parseInt(editForm.release_year) : null,
            rating: editForm.rating ? parseFloat(editForm.rating) : null,
            episodes: editForm.episodes ? parseInt(editForm.episodes) : null
          })
        }
      );
      
      const data = await response.json();
      
      if (data.success) {
        setMessage({ type: 'success', text: '更新成功！' });
        fetchAnimes(pagination.page, searchKeyword);
        setSelectedAnime(null);
      } else {
        setMessage({ type: 'error', text: data.error || '更新失败' });
      }
    } catch (error) {
      console.error('更新失败:', error);
      setMessage({ type: 'error', text: '更新失败' });
    }
  };

  // 选择动漫进行编辑
  const selectAnime = (anime: Anime) => {
    setSelectedAnime(anime);
    setEditForm({
      title: anime.title || '',
      title_jp: anime.title_jp || '',
      cover_image: anime.cover_image || '',
      studio: anime.studio || '',
      release_year: anime.release_year?.toString() || '',
      description: '',
      episodes: '',
      status: '',
      genre: '',
      rating: anime.rating?.toString() || ''
    });
    setBangumiSearch(anime.title);
    setBangumiResults([]);
  };

  // 清除消息
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => setMessage(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [message]);

  if (!isAdmin) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <h2>⚠️ 无权限访问</h2>
        <p>只有管理员可以访问此页面</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1400px', margin: '0 auto' }}>
      <h1>🎬 动漫图片管理后台</h1>
      <p style={{ color: '#666', marginBottom: '20px' }}>
        当前共有 {pagination.total} 个动漫需要修复图片
      </p>

      {/* 消息提示 */}
      {message && (
        <div style={{
          padding: '12px 20px',
          borderRadius: '8px',
          marginBottom: '20px',
          backgroundColor: message.type === 'success' ? '#d4edda' : '#f8d7da',
          color: message.type === 'success' ? '#155724' : '#721c24'
        }}>
          {message.text}
        </div>
      )}

      <div style={{ display: 'flex', gap: '20px' }}>
        {/* 左侧：动漫列表 */}
        <div style={{ flex: 1, minWidth: 0 }}>
          {/* 搜索和筛选 */}
          <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
            <input
              type="text"
              placeholder="搜索动漫..."
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && fetchAnimes(1, searchKeyword)}
              style={{
                flex: 1,
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '6px'
              }}
            />
            <button
              onClick={() => fetchAnimes(1, searchKeyword)}
              style={{
                padding: '10px 20px',
                backgroundColor: '#4a90d9',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              搜索
            </button>
          </div>

          {/* 动漫列表 */}
          <div style={{
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            maxHeight: '70vh',
            overflow: 'auto'
          }}>
            {loading ? (
              <div style={{ padding: '40px', textAlign: 'center' }}>加载中...</div>
            ) : (
              animes.map((anime) => (
                <div
                  key={anime.id}
                  onClick={() => selectAnime(anime)}
                  style={{
                    display: 'flex',
                    gap: '12px',
                    padding: '12px',
                    borderBottom: '1px solid #e0e0e0',
                    cursor: 'pointer',
                    backgroundColor: selectedAnime?.id === anime.id ? '#f0f7ff' : 'white',
                    transition: 'background-color 0.2s'
                  }}
                >
                  <img
                    src={anime.cover_image}
                    alt={anime.title}
                    style={{
                      width: '60px',
                      height: '80px',
                      objectFit: 'cover',
                      borderRadius: '4px'
                    }}
                  />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: '600', marginBottom: '4px' }}>
                      {anime.title}
                    </div>
                    {anime.title_jp && (
                      <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>
                        {anime.title_jp}
                      </div>
                    )}
                    <div style={{ fontSize: '12px', color: '#888' }}>
                      {anime.studio && `🏠 ${anime.studio}`}
                      {anime.release_year && ` · 📅 ${anime.release_year}`}
                      {anime.rating && ` · ⭐ ${anime.rating}`}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* 分页 */}
          <div style={{
            marginTop: '20px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            gap: '10px'
          }}>
            <button
              onClick={() => fetchAnimes(pagination.page - 1, searchKeyword)}
              disabled={pagination.page <= 1}
              style={{
                padding: '8px 16px',
                border: '1px solid #ddd',
                borderRadius: '6px',
                cursor: pagination.page <= 1 ? 'not-allowed' : 'pointer',
                opacity: pagination.page <= 1 ? 0.5 : 1
              }}
            >
              上一页
            </button>
            <span style={{ color: '#666' }}>
              第 {pagination.page} 页 / 共 {pagination.totalPages} 页
            </span>
            <button
              onClick={() => fetchAnimes(pagination.page + 1, searchKeyword)}
              disabled={pagination.page >= pagination.totalPages}
              style={{
                padding: '8px 16px',
                border: '1px solid #ddd',
                borderRadius: '6px',
                cursor: pagination.page >= pagination.totalPages ? 'not-allowed' : 'pointer',
                opacity: pagination.page >= pagination.totalPages ? 0.5 : 1
              }}
            >
              下一页
            </button>
          </div>
        </div>

        {/* 右侧：编辑和搜索 */}
        <div style={{ width: '500px', minWidth: '400px' }}>
          {selectedAnime ? (
            <div>
              <h2>✏️ 编辑动漫</h2>
              
              {/* 当前动漫信息 */}
              <div style={{
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                padding: '16px',
                marginBottom: '20px',
                backgroundColor: '#fafafa'
              }}>
                <div style={{ display: 'flex', gap: '16px' }}>
                  <img
                    src={selectedAnime.cover_image}
                    alt={selectedAnime.title}
                    style={{
                      width: '120px',
                      height: '160px',
                      objectFit: 'cover',
                      borderRadius: '8px'
                    }}
                  />
                  <div style={{ flex: 1 }}>
                    <h3 style={{ margin: '0 0 8px 0' }}>{selectedAnime.title}</h3>
                    {selectedAnime.title_jp && (
                      <p style={{ margin: '0 0 8px 0', color: '#666' }}>
                        {selectedAnime.title_jp}
                      </p>
                    )}
                    <p style={{ margin: '4px 0', fontSize: '14px', color: '#888' }}>
                      ID: {selectedAnime.id}
                    </p>
                  </div>
                </div>
              </div>

              {/* Bangumi搜索 */}
              <div style={{ marginBottom: '20px' }}>
                <h3>🔍 从 Bangumi 搜索</h3>
                <div style={{ display: 'flex', gap: '10px', marginBottom: '12px' }}>
                  <input
                    type="text"
                    value={bangumiSearch}
                    onChange={(e) => setBangumiSearch(e.target.value)}
                    placeholder="输入关键词搜索..."
                    style={{
                      flex: 1,
                      padding: '10px',
                      border: '1px solid #ddd',
                      borderRadius: '6px'
                    }}
                  />
                  <button
                    onClick={searchBangumi}
                    disabled={bangumiLoading}
                    style={{
                      padding: '10px 20px',
                      backgroundColor: '#4a90d9',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: bangumiLoading ? 'not-allowed' : 'pointer'
                    }}
                  >
                    {bangumiLoading ? '搜索中...' : '搜索'}
                  </button>
                </div>

                {/* Bangumi搜索结果 */}
                {bangumiResults.length > 0 && (
                  <div style={{
                    border: '1px solid #e0e0e0',
                    borderRadius: '8px',
                    maxHeight: '400px',
                    overflow: 'auto'
                  }}>
                    {bangumiResults.map((result) => (
                      <div
                        key={result.id}
                        style={{
                          display: 'flex',
                          gap: '12px',
                          padding: '12px',
                          borderBottom: '1px solid #e0e0e0'
                        }}
                      >
                        <img
                          src={result.cover}
                          alt={result.title_cn || result.title}
                          style={{
                            width: '60px',
                            height: '80px',
                            objectFit: 'cover',
                            borderRadius: '4px'
                          }}
                        />
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div style={{ fontWeight: '600', marginBottom: '4px' }}>
                            {result.title_cn || result.title}
                          </div>
                          {result.title_cn && result.title !== result.title_cn && (
                            <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>
                              {result.title}
                            </div>
                          )}
                          <div style={{ fontSize: '12px', color: '#888', marginBottom: '8px' }}>
                            {result.score && `⭐ ${result.score}`}
                            {result.air_date && ` · 📅 ${result.air_date}`}
                          </div>
                          <button
                            onClick={() => importFromBangumi(selectedAnime.id, result.id)}
                            style={{
                              padding: '6px 12px',
                              backgroundColor: '#28a745',
                              color: 'white',
                              border: 'none',
                              borderRadius: '4px',
                              cursor: 'pointer',
                              fontSize: '12px'
                            }}
                          >
                            📥 导入此条
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* 手动编辑 */}
              <div>
                <h3>✏️ 手动编辑</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  <div>
                    <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                      中文标题
                    </label>
                    <input
                      type="text"
                      value={editForm.title}
                      onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                      style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #ddd',
                        borderRadius: '6px'
                      }}
                    />
                  </div>
                  
                  <div>
                    <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                      日文标题
                    </label>
                    <input
                      type="text"
                      value={editForm.title_jp}
                      onChange={(e) => setEditForm({ ...editForm, title_jp: e.target.value })}
                      style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #ddd',
                        borderRadius: '6px'
                      }}
                    />
                  </div>
                  
                  <div>
                    <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                      封面图片URL
                    </label>
                    <input
                      type="text"
                      value={editForm.cover_image}
                      onChange={(e) => setEditForm({ ...editForm, cover_image: e.target.value })}
                      placeholder="https://..."
                      style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #ddd',
                        borderRadius: '6px'
                      }}
                    />
                  </div>
                  
                  <div>
                    <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                      工作室
                    </label>
                    <input
                      type="text"
                      value={editForm.studio}
                      onChange={(e) => setEditForm({ ...editForm, studio: e.target.value })}
                      style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #ddd',
                        borderRadius: '6px'
                      }}
                    />
                  </div>
                  
                  <div style={{ display: 'flex', gap: '12px' }}>
                    <div style={{ flex: 1 }}>
                      <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                        年份
                      </label>
                      <input
                        type="number"
                        value={editForm.release_year}
                        onChange={(e) => setEditForm({ ...editForm, release_year: e.target.value })}
                        style={{
                          width: '100%',
                          padding: '10px',
                          border: '1px solid #ddd',
                          borderRadius: '6px'
                        }}
                      />
                    </div>
                    <div style={{ flex: 1 }}>
                      <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                        评分
                      </label>
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        max="10"
                        value={editForm.rating}
                        onChange={(e) => setEditForm({ ...editForm, rating: e.target.value })}
                        style={{
                          width: '100%',
                          padding: '10px',
                          border: '1px solid #ddd',
                          borderRadius: '6px'
                        }}
                      />
                    </div>
                  </div>
                  
                  <div style={{ display: 'flex', gap: '10px', marginTop: '8px' }}>
                    <button
                      onClick={updateAnime}
                      style={{
                        flex: 1,
                        padding: '12px',
                        backgroundColor: '#4a90d9',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '500'
                      }}
                    >
                      💾 保存修改
                    </button>
                    <button
                      onClick={() => setSelectedAnime(null)}
                      style={{
                        padding: '12px 20px',
                        backgroundColor: '#6c757d',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer'
                      }}
                    >
                      取消
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div style={{
              border: '2px dashed #ddd',
              borderRadius: '12px',
              padding: '60px 20px',
              textAlign: 'center',
              color: '#888'
            }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>🎬</div>
              <h3 style={{ margin: '0 0 8px 0' }}>选择一个动漫</h3>
              <p>从左侧列表中选择一个动漫来编辑或搜索真实图片</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnimeManagerPage;
