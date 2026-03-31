import express from 'express';
import mysql from 'mysql2/promise';
import axios from 'axios';

const router = express.Router();

// 数据库连接配置
const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

// Bangumi API 搜索动漫
router.get('/search-bangumi', async (req, res) => {
  try {
    const { keyword } = req.query;
    
    if (!keyword) {
      return res.status(400).json({ error: '请提供搜索关键词' });
    }

    // 使用 Bangumi API 搜索
    const response = await axios.get(`https://api.bgm.tv/search/subject/${encodeURIComponent(keyword as string)}`, {
      params: {
        type: 2, // 2 = 动画
        responseGroup: 'small'
      },
      timeout: 10000
    });

    const results = response.data.list?.map((item: any) => ({
      id: item.id,
      title: item.name,
      title_cn: item.name_cn,
      cover: item.images?.large || item.images?.common || item.images?.medium,
      summary: item.summary,
      score: item.rating?.score,
      air_date: item.air_date
    })) || [];

    res.json({ results });
  } catch (error) {
    console.error('Bangumi API 搜索错误:', error);
    res.status(500).json({ error: '搜索失败，请稍后重试' });
  }
});

// 获取 Bangumi 动漫详情
router.get('/bangumi-detail/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const response = await axios.get(`https://api.bgm.tv/subject/${id}`, {
      params: {
        responseGroup: 'large'
      },
      timeout: 10000
    });

    const data = response.data;
    
    res.json({
      title: data.name,
      title_cn: data.name_cn,
      cover: data.images?.large || data.images?.common,
      summary: data.summary,
      score: data.rating?.score,
      air_date: data.air_date,
      eps: data.eps,
      eps_count: data.eps_count,
      staff: data.staff,
      characters: data.characters
    });
  } catch (error) {
    console.error('Bangumi API 详情错误:', error);
    res.status(500).json({ error: '获取详情失败' });
  }
});

// 更新动漫信息
router.put('/:id', async (req, res) => {
  let connection;
  try {
    const { id } = req.params;
    const {
      title,
      title_jp,
      cover_image,
      studio,
      release_year,
      description,
      episodes,
      status,
      genre,
      rating
    } = req.body;

    connection = await mysql.createConnection(dbConfig);
    
    const query = `
      UPDATE animes 
      SET title = COALESCE(?, title),
          title_jp = COALESCE(?, title_jp),
          cover_image = COALESCE(?, cover_image),
          studio = COALESCE(?, studio),
          release_year = COALESCE(?, release_year),
          description = COALESCE(?, description),
          episodes = COALESCE(?, episodes),
          status = COALESCE(?, status),
          genre = COALESCE(?, genre),
          rating = COALESCE(?, rating),
          updated_at = NOW()
      WHERE id = ?
    `;

    const [result] = await connection.execute(query, [
      title,
      title_jp,
      cover_image,
      studio,
      release_year,
      description,
      episodes,
      status,
      genre,
      rating,
      id
    ]);

    // 获取更新后的动漫信息
    const [updated] = await connection.execute(
      'SELECT * FROM animes WHERE id = ?',
      [id]
    );

    res.json({
      success: true,
      message: '更新成功',
      anime: (updated as any)[0]
    });
  } catch (error) {
    console.error('更新动漫错误:', error);
    res.status(500).json({ error: '更新失败' });
  } finally {
    if (connection) {
      await connection.end();
    }
  }
});

// 从 Bangumi 导入动漫信息
router.post('/import-from-bangumi/:animeId', async (req, res) => {
  let connection;
  try {
    const { animeId } = req.params;
    const { bangumiId } = req.body;

    connection = await mysql.createConnection(dbConfig);

    // 获取 Bangumi 详情
    const bangumiResponse = await axios.get(`https://api.bgm.tv/subject/${bangumiId}`, {
      params: { responseGroup: 'large' },
      timeout: 10000
    });

    const bangumiData = bangumiResponse.data;
    
    // 更新本地数据库
    const query = `
      UPDATE animes 
      SET title = COALESCE(?, title),
          title_jp = COALESCE(?, title_jp),
          cover_image = COALESCE(?, cover_image),
          description = COALESCE(?, description),
          rating = COALESCE(?, rating),
          updated_at = NOW()
      WHERE id = ?
    `;

    await connection.execute(query, [
      bangumiData.name_cn || bangumiData.name,
      bangumiData.name,
      bangumiData.images?.large || bangumiData.images?.common,
      bangumiData.summary,
      bangumiData.rating?.score,
      animeId
    ]);

    // 获取更新后的信息
    const [updated] = await connection.execute(
      'SELECT * FROM animes WHERE id = ?',
      [animeId]
    );

    res.json({
      success: true,
      message: '导入成功',
      anime: (updated as any)[0]
    });
  } catch (error) {
    console.error('从 Bangumi 导入错误:', error);
    res.status(500).json({ error: '导入失败' });
  } finally {
    if (connection) {
      await connection.end();
    }
  }
});

// 获取需要修复的动漫列表（分页）
router.get('/needs-fix', async (req, res) => {
  let connection;
  try {
    const { page = 1, limit = 20, search = '' } = req.query;
    const offset = (Number(page) - 1) * Number(limit);

    connection = await mysql.createConnection(dbConfig);

    let whereClause = "WHERE cover_image LIKE '%picsum.photos%'";
    const params: any[] = [];

    if (search) {
      whereClause += " AND (title LIKE ? OR title_jp LIKE ?)";
      params.push(`%${search}%`, `%${search}%`);
    }

    // 获取总数
    const [countResult] = await connection.execute(
      `SELECT COUNT(*) as total FROM animes ${whereClause}`,
      params
    );
    const total = (countResult as any)[0].total;

    // 获取数据
    const [animes] = await connection.execute(
      `SELECT id, title, title_jp, cover_image, studio, release_year, rating 
       FROM animes 
       ${whereClause}
       ORDER BY id DESC
       LIMIT ? OFFSET ?`,
      [...params, Number(limit), offset]
    );

    res.json({
      animes,
      pagination: {
        page: Number(page),
        limit: Number(limit),
        total,
        totalPages: Math.ceil(total / Number(limit))
      }
    });
  } catch (error) {
    console.error('获取需要修复的动漫列表错误:', error);
    res.status(500).json({ error: '获取列表失败' });
  } finally {
    if (connection) {
      await connection.end();
    }
  }
});

export default router;
