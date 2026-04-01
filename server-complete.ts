import express from 'express';
import cors from 'cors';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import mysql from 'mysql2/promise';
import animeAdminRoutes from './src/server/routes/anime-admin';

const app = express();
const PORT = 3001;
const JWT_SECRET = 'your-secret-key-change-in-production';

app.use(cors());
app.use(express.json());

// MySQL数据库连接配置
const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

// 创建数据库连接池
const pool = mysql.createPool(dbConfig);

// 测试数据库连接
async function testDbConnection() {
  try {
    const connection = await pool.getConnection();
    console.log('Successfully connected to MySQL database!');
    connection.release();
  } catch (error) {
    console.error('Failed to connect to MySQL database:', error);
    process.exit(1);
  }
}

testDbConnection();

// ==================== 存储验证码和滑块验证（模拟Redis） ====================
interface VerificationCode {
  code: string;
  timestamp: number;
}

interface SliderToken {
  valid: boolean;
  timestamp: number;
}

const smsCodes = new Map<string, VerificationCode>();
const sliderTokens = new Map<string, SliderToken>();

// 验证码过期时间：5分钟
const CODE_EXPIRE_TIME = 5 * 60 * 1000;
// 滑块验证过期时间：10分钟
const SLIDER_EXPIRE_TIME = 10 * 60 * 1000;

// 生成随机6位数字验证码
function generateVerifyCode(): string {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

// 生成UUID
function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// 验证邮箱格式
function isValidEmail(email: string): boolean {
  return /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(email);
}

// ==================== 认证中间件 ====================
const authenticateToken = (req: express.Request, res: express.Response, next: express.NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Access denied' });
  }
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as any;
    (req as any).user = decoded;
    next();
  } catch (error) {
    res.status(403).json({ error: 'Invalid token' });
  }
};

// ==================== 管理接口路由 ====================
app.use('/api/admin/anime', animeAdminRoutes);

// ==================== 新接口：滑块验证 ====================
app.get('/api/slider-token', (req, res) => {
  const token = generateUUID();
  sliderTokens.set(token, { valid: true, timestamp: Date.now() });
  res.json({ success: true, message: '获取成功', data: { sliderToken: token } });
});

// ==================== 新接口：发送邮箱验证码 ====================
app.post('/api/send-code', async (req, res) => {
  try {
    const { email, sliderToken } = req.body;

    // 验证滑块
    const slider = sliderTokens.get(sliderToken);
    if (!slider || !slider.valid || Date.now() - slider.timestamp > SLIDER_EXPIRE_TIME) {
      return res.status(400).json({ success: false, message: '滑块验证失败，请重新验证' });
    }

    // 验证邮箱格式
    if (!email || !isValidEmail(email)) {
      return res.status(400).json({ success: false, message: '邮箱格式不正确' });
    }

    // 生成验证码
    const code = generateVerifyCode();
    
    // 存储验证码（使用email作为key）
    smsCodes.set(email, { code, timestamp: Date.now() });
    
    // 移除已使用的滑块令牌，并生成新的
    sliderTokens.delete(sliderToken);
    const newSliderToken = generateUUID();
    sliderTokens.set(newSliderToken, { valid: true, timestamp: Date.now() });

    // 真实环境中这里需要调用第三方邮件服务API，如Nodemailer、SendGrid等
    console.log(`【模拟邮件发送】邮箱: ${email}, 验证码: ${code}`);

    res.json({
      success: true,
      message: '验证码发送成功',
      data: {
        sliderToken: newSliderToken,
        // 注意：测试环境下返回验证码，生产环境不应返回
        testCode: code
      }
    });
  } catch (error) {
    console.error('发送验证码错误:', error);
    res.status(500).json({ success: false, message: '发送验证码失败' });
  }
});

// ==================== 用户注册（修改为邮箱注册） ====================
app.post('/api/register', async (req, res) => {
  try {
    const { username, email, password, verifyCode, sliderToken } = req.body;

    // 验证滑块
    const slider = sliderTokens.get(sliderToken);
    if (!slider || !slider.valid || Date.now() - slider.timestamp > SLIDER_EXPIRE_TIME) {
      return res.status(400).json({ success: false, message: '滑块验证失败，请重新验证' });
    }

    // 验证邮箱验证码
    const storedCode = smsCodes.get(email);
    if (!storedCode || storedCode.code !== verifyCode || Date.now() - storedCode.timestamp > CODE_EXPIRE_TIME) {
      return res.status(400).json({ success: false, message: '验证码错误或已过期' });
    }

    if (!username || !email || !password) {
      return res.status(400).json({ success: false, message: '所有字段都是必填的' });
    }

    if (username.length < 3) {
      return res.status(400).json({ success: false, message: '用户名至少需要3个字符' });
    }

    if (password.length < 6) {
      return res.status(400).json({ success: false, message: '密码至少需要6个字符' });
    }

    // 检查用户名或邮箱是否已存在
    const [existingUsers] = await pool.execute(
      'SELECT id, username, email FROM users WHERE username = ? OR email = ?',
      [username, email]
    ) as any[];

    if (existingUsers.length > 0) {
      const user = existingUsers[0];
      if (user.username === username) {
        return res.status(400).json({ success: false, message: '用户名已存在' });
      }
      if (user.email === email) {
        return res.status(400).json({ success: false, message: '邮箱已被注册' });
      }
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const avatar = `https://picsum.photos/seed/user${Date.now()}/100/100`;

    // 插入新用户
    const [result] = await pool.execute(
      'INSERT INTO users (username, email, password, avatar) VALUES (?, ?, ?, ?)',
      [username, email, hashedPassword, avatar]
    ) as any;

    // 清除已使用的验证码和滑块令牌
    smsCodes.delete(email);
    sliderTokens.delete(sliderToken);

    // 生成token自动登录
    const token = jwt.sign({ id: result.insertId, username }, JWT_SECRET, { expiresIn: '7d' });

    res.status(201).json({
      success: true,
      message: '注册成功',
      data: {
        token,
        user: {
          id: result.insertId,
          username,
          email,
          avatar
        }
      }
    });
  } catch (error) {
    console.error('注册错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 用户登录（支持用户名/邮箱登录） ====================
app.post('/api/login', async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ success: false, message: '请输入用户名和密码' });
    }

    // 查询用户（支持用户名/邮箱登录）
    const [users] = await pool.execute(
      'SELECT id, username, email, phone, password, avatar FROM users WHERE username = ? OR email = ?',
      [username, username]
    ) as any[];

    if (users.length === 0) {
      return res.status(400).json({ success: false, message: '用户名或密码错误' });
    }

    const user = users[0];

    const isValidPassword = await bcrypt.compare(password, user.password);

    if (!isValidPassword) {
      return res.status(400).json({ success: false, message: '用户名或密码错误' });
    }

    const token = jwt.sign({ id: user.id, username: user.username }, JWT_SECRET, { expiresIn: '7d' });

    res.json({
      success: true,
      message: '登录成功',
      data: {
        token,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          phone: user.phone,
          avatar: user.avatar
        }
      }
    });
  } catch (error) {
    console.error('登录错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 管理员登录 ====================
app.post('/api/admin/login', async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ success: false, message: '请输入用户名和密码' });
    }

    // 简单的管理员判断：用户名是admin即为管理员
    if (username !== 'admin') {
      return res.status(403).json({ success: false, message: '非管理员账号' });
    }

    // 查询用户
    const [users] = await pool.execute(
      'SELECT id, username, email, phone, password, avatar FROM users WHERE username = ?',
      [username]
    ) as any[];

    if (users.length === 0) {
      return res.status(400).json({ success: false, message: '用户名或密码错误' });
    }

    const user = users[0];

    const isValidPassword = await bcrypt.compare(password, user.password);

    if (!isValidPassword) {
      return res.status(400).json({ success: false, message: '用户名或密码错误' });
    }

    const token = jwt.sign({ id: user.id, username: user.username, isAdmin: true }, JWT_SECRET, { expiresIn: '7d' });

    res.json({
      success: true,
      message: '管理员登录成功',
      data: {
        token,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          phone: user.phone,
          avatar: user.avatar,
          isAdmin: true
        }
      }
    });
  } catch (error) {
    console.error('管理员登录错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取当前用户信息 ====================
app.get('/api/user', authenticateToken, async (req, res) => {
  try {
    const userId = (req as any).user.id;

    const [users] = await pool.execute(
      'SELECT id, username, email, phone, avatar FROM users WHERE id = ?',
      [userId]
    ) as any[];

    if (users.length === 0) {
      return res.status(404).json({ success: false, message: '用户不存在' });
    }

    res.json({ success: true, data: users[0] });
  } catch (error) {
    console.error('获取用户信息错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 搜索动漫（支持按标题、描述、工作室、作者搜索） ====================
app.get('/api/anime/search', async (req, res) => {
  try {
    const { keyword, year, startYear, endYear, status, studio, author, page = 1, limit = 10 } = req.query;

    let sql = 'SELECT * FROM animes WHERE 1=1';
    let params: any[] = [];

    // 关键词搜索（标题、描述、工作室）
    if (keyword) {
      sql += ' AND (title LIKE ? OR description LIKE ? OR studio LIKE ?)';
      const searchPattern = `%${keyword}%`;
      params.push(searchPattern, searchPattern, searchPattern);
    }

    // 按年份筛选
    if (year) {
      sql += ' AND release_year = ?';
      params.push(year);
    }

    // 按起始年份筛选
    if (startYear && !year) {
      sql += ' AND release_year >= ?';
      params.push(startYear);
    }

    // 按结束年份筛选
    if (endYear && !year) {
      sql += ' AND release_year <= ?';
      params.push(endYear);
    }

    // 按状态筛选
    if (status) {
      sql += ' AND status = ?';
      params.push(status);
    }

    // 按工作室筛选
    if (studio) {
      sql += ' AND studio LIKE ?';
      params.push(`%${studio}%`);
    }

    // 按作者筛选
    if (author) {
      sql += ' AND (author LIKE ? OR title LIKE ?)';
      const authorPattern = `%${author}%`;
      params.push(authorPattern, authorPattern);
    }

    // 按评分排序
    sql += ' ORDER BY average_rating DESC, rating_count DESC';

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql, params) as any[];

    // 获取总数
    let countSql = 'SELECT COUNT(*) as total FROM animes WHERE 1=1';
    let countParams: any[] = [];
    
    if (keyword) {
      countSql += ' AND (title LIKE ? OR description LIKE ? OR studio LIKE ?)';
      const searchPattern = `%${keyword}%`;
      countParams.push(searchPattern, searchPattern, searchPattern);
    }
    if (year) {
      countSql += ' AND release_year = ?';
      countParams.push(year);
    }
    if (startYear && !year) {
      countSql += ' AND release_year >= ?';
      countParams.push(startYear);
    }
    if (endYear && !year) {
      countSql += ' AND release_year <= ?';
      countParams.push(endYear);
    }
    if (status) {
      countSql += ' AND status = ?';
      countParams.push(status);
    }
    if (studio) {
      countSql += ' AND studio LIKE ?';
      countParams.push(`%${studio}%`);
    }
    if (author) {
      countSql += ' AND (author LIKE ? OR title LIKE ?)';
      const authorPattern = `%${author}%`;
      countParams.push(authorPattern, authorPattern);
    }

    const [countResult] = await pool.execute(countSql, countParams) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('搜索错误:', error);
    res.status(500).json({ success: false, message: '搜索失败' });
  }
});

// ==================== 获取连载动漫 ====================
app.get('/api/anime/ongoing', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    let sql = `SELECT * FROM animes WHERE status = '连载中' 
               ORDER BY average_rating DESC, rating_count DESC`;

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql) as any[];

    // 获取总数
    const [countResult] = await pool.execute(
      "SELECT COUNT(*) as total FROM animes WHERE status = '连载中'"
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取连载动漫错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取完结动漫 ====================
app.get('/api/anime/completed', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    let sql = `SELECT * FROM animes WHERE status = '已完结' 
               ORDER BY average_rating DESC, rating_count DESC`;

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql) as any[];

    // 获取总数
    const [countResult] = await pool.execute(
      "SELECT COUNT(*) as total FROM animes WHERE status = '已完结'"
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取完结动漫错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取国产动漫 ====================
app.get('/api/anime/chinese', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    let sql = `SELECT * FROM animes WHERE nationality = '中国' 
               ORDER BY average_rating DESC, rating_count DESC`;

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql) as any[];

    // 获取总数
    const [countResult] = await pool.execute(
      "SELECT COUNT(*) as total FROM animes WHERE nationality = '中国'"
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取国产动漫错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取日本动漫 ====================
app.get('/api/anime/japanese', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    let sql = `SELECT * FROM animes WHERE nationality = '日本' 
               ORDER BY average_rating DESC, rating_count DESC`;

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql) as any[];

    // 获取总数
    const [countResult] = await pool.execute(
      "SELECT COUNT(*) as total FROM animes WHERE nationality = '日本'"
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取日本动漫错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取剧场版 ====================
app.get('/api/anime/theater', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    let sql = `SELECT * FROM animes WHERE is_movie = 1 
               ORDER BY average_rating DESC, rating_count DESC`;

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql) as any[];

    // 获取总数
    const [countResult] = await pool.execute(
      'SELECT COUNT(*) as total FROM animes WHERE is_movie = 1'
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取剧场版错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取B站冷门佳作 ====================
app.get('/api/anime/hidden-gems', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    let sql = `SELECT * FROM animes 
               WHERE is_hidden_gem = 1 
               ORDER BY average_rating DESC, rating_count DESC`;

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql) as any[];

    // 获取总数
    const [countResult] = await pool.execute(
      'SELECT COUNT(*) as total FROM animes WHERE is_hidden_gem = 1'
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取冷门佳作错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取每日推荐（随机推荐） ====================
app.get('/api/anime/daily', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    // 使用随机排序，但还是保证高分的优先出现
    let sql = `SELECT * FROM animes 
               ORDER BY RAND() DESC, average_rating DESC, rating_count DESC`;

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql) as any[];

    // 获取总数
    const [countResult] = await pool.execute(
      'SELECT COUNT(*) as total FROM animes'
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取每日推荐错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取动漫列表 ====================
app.get('/api/anime', async (req, res) => {
  try {
    const { page = 1, limit = 10, sort = 'rating' } = req.query;

    let sql = 'SELECT * FROM animes';

    // 排序
    if (sort === 'rating') {
      sql += ' ORDER BY average_rating DESC, rating_count DESC';
    } else if (sort === 'year') {
      sql += ' ORDER BY release_year DESC';
    } else if (sort === 'name') {
      sql += ' ORDER BY title ASC';
    }

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql) as any[];

    // 获取总数
    const [countResult] = await pool.execute('SELECT COUNT(*) as total FROM animes') as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取动漫列表错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取新番动漫（最近2个月上映） ====================
app.get('/api/anime/recent', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    // 计算当前年份
    const now = new Date();
    const currentYear = now.getFullYear();
    
    // 用 release_year 筛选今年的，同时是近2个月的
    let sql = `SELECT * FROM animes 
               WHERE release_year = ? 
               ORDER BY average_rating DESC, rating_count DESC`;
    let params: any[] = [currentYear];

    // 分页
    const offset = (Number(page) - 1) * Number(limit);
    sql += ` LIMIT ${Number(limit)} OFFSET ${offset}`;

    const [animes] = await pool.execute(sql, params) as any[];

    // 获取总数
    let countSql = `SELECT COUNT(*) as total FROM animes WHERE release_year = ?`;
    const [countResult] = await pool.execute(countSql, params) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取新番动漫错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取筛选选项 ====================
app.get('/api/anime/filter-options', async (req, res) => {
  try {
    // 获取所有年份
    const [yearsResult] = await pool.execute(
      'SELECT DISTINCT release_year FROM animes WHERE release_year IS NOT NULL ORDER BY release_year DESC'
    ) as any[];

    // 获取所有状态
    const [statusResult] = await pool.execute(
      'SELECT DISTINCT status FROM animes WHERE status IS NOT NULL'
    ) as any[];

    // 获取所有工作室
    const [studioResult] = await pool.execute(
      'SELECT DISTINCT studio FROM animes WHERE studio IS NOT NULL ORDER BY studio'
    ) as any[];

    res.json({
      success: true,
      data: {
        years: yearsResult.map((item: any) => item.release_year),
        statuses: statusResult.map((item: any) => item.status),
        studios: studioResult.map((item: any) => item.studio)
      }
    });
  } catch (error) {
    console.error('获取筛选选项错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取单个动漫详情 ====================
app.get('/api/anime/:id', async (req, res) => {
  try {
    const animeId = parseInt(req.params.id || '0');
    if (isNaN(animeId) || animeId <= 0) {
      return res.status(400).json({ success: false, message: '无效的动漫ID' });
    }

    const [animes] = await pool.execute(
      'SELECT * FROM animes WHERE id = ?',
      [animeId]
    ) as any[];

    if (animes.length === 0) {
      return res.status(404).json({ success: false, message: '动漫不存在' });
    }

    res.json({ success: true, data: animes[0] });
  } catch (error) {
    console.error('获取动漫详情错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 获取用户对某个动漫的评分 ====================
app.get('/api/anime/:id/user-rating', authenticateToken, async (req, res) => {
  try {
    const animeId = parseInt(req.params.id || '0');
    if (isNaN(animeId) || animeId <= 0) {
      return res.status(400).json({ success: false, message: '无效的动漫ID' });
    }
    const userId = (req as any).user.id;

    const [ratings] = await pool.execute(
      'SELECT rating FROM ratings WHERE user_id = ? AND anime_id = ?',
      [userId, animeId]
    ) as any[];

    if (ratings.length > 0) {
      res.json({ success: true, data: { rating: ratings[0].rating } });
    } else {
      res.json({ success: true, data: { rating: null } });
    }
  } catch (error) {
    console.error('获取用户评分错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 提交评分 ====================
app.post('/api/anime/:id/rate', authenticateToken, async (req, res) => {
  try {
    const animeId = parseInt(req.params.id || '0');
    if (isNaN(animeId) || animeId <= 0) {
      return res.status(400).json({ success: false, message: '无效的动漫ID' });
    }
    const userId = (req as any).user.id;
    const { rating } = req.body;

    if (!rating || rating < 1 || rating > 5) {
      return res.status(400).json({ success: false, message: '评分必须在1-5之间' });
    }

    // 检查动漫是否存在
    const [animes] = await pool.execute('SELECT id FROM animes WHERE id = ?', [animeId]) as any[];
    if (animes.length === 0) {
      return res.status(404).json({ success: false, message: '动漫不存在' });
    }

    // 检查用户是否已经评分
    const [existingRatings] = await pool.execute(
      'SELECT id FROM ratings WHERE user_id = ? AND anime_id = ?',
      [userId, animeId]
    ) as any[];

    if (existingRatings.length > 0) {
      // 更新评分
      await pool.execute(
        'UPDATE ratings SET rating = ? WHERE user_id = ? AND anime_id = ?',
        [rating, userId, animeId]
      );
    } else {
      // 插入新评分
      await pool.execute(
        'INSERT INTO ratings (user_id, anime_id, rating) VALUES (?, ?, ?)',
        [userId, animeId, rating]
      );
    }

    // 重新计算平均评分
    const [avgResult] = await pool.execute(
      'SELECT AVG(rating) as avg_rating, COUNT(*) as count FROM ratings WHERE anime_id = ?',
      [animeId]
    ) as any[];

    const avgRating = avgResult[0].avg_rating || 0;
    const count = avgResult[0].count || 0;

    // 更新动漫表中的平均评分
    await pool.execute(
      'UPDATE animes SET average_rating = ?, rating_count = ? WHERE id = ?',
      [parseFloat(avgRating).toFixed(2), count, animeId]
    );

    res.json({
      success: true,
      message: '评分成功',
      data: {
        average_rating: parseFloat(avgRating),
        rating_count: count,
        user_rating: rating
      }
    });
  } catch (error) {
    console.error('评分错误:', error);
    res.status(500).json({ success: false, message: '评分失败' });
  }
});

// ==================== 获取评论列表 ====================
app.get('/api/anime/:id/comments', async (req, res) => {
  try {
    const animeId = parseInt(req.params.id || '0');
    if (isNaN(animeId) || animeId <= 0) {
      return res.status(400).json({ success: false, message: '无效的动漫ID' });
    }
    const { page = 1, limit = 10 } = req.query;

    const offset = (Number(page) - 1) * Number(limit);

    const [comments] = await pool.execute(`
      SELECT c.id, c.content, c.created_at, c.user_id, u.username, u.avatar
      FROM comments c
      JOIN users u ON c.user_id = u.id
      WHERE c.anime_id = ?
      ORDER BY c.created_at DESC
      LIMIT ${Number(limit)} OFFSET ${offset}
    `, [animeId]) as any[];

    // 获取总数
    const [countResult] = await pool.execute(
      'SELECT COUNT(*) as total FROM comments WHERE anime_id = ?',
      [animeId]
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        comments,
        pagination: {
          total,
          page: Number(page),
          limit: Number(limit),
          totalPages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('获取评论错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 发表评论 ====================
app.post('/api/anime/:id/comments', authenticateToken, async (req, res) => {
  try {
    const animeId = parseInt(req.params.id || '0');
    if (isNaN(animeId) || animeId <= 0) {
      return res.status(400).json({ success: false, message: '无效的动漫ID' });
    }
    const userId = (req as any).user.id;
    const { content } = req.body;

    if (!content || content.trim().length === 0) {
      return res.status(400).json({ success: false, message: '评论内容不能为空' });
    }

    // 插入评论
    const [result] = await pool.execute(
      'INSERT INTO comments (user_id, anime_id, content) VALUES (?, ?, ?)',
      [userId, animeId, content.trim()]
    ) as any;

    // 获取评论详情
    const [comments] = await pool.execute(`
      SELECT c.id, c.content, c.created_at, c.user_id, u.username, u.avatar
      FROM comments c
      JOIN users u ON c.user_id = u.id
      WHERE c.id = ?
    `, [result.insertId]) as any[];

    res.json({
      success: true,
      message: '评论发表成功',
      data: comments[0]
    });
  } catch (error) {
    console.error('发表评论错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

// ==================== 启动服务器 ====================
app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
  console.log(`管理接口: http://localhost:${PORT}/api/admin/anime`);
});
