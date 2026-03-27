import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show=True):
    if show:
        print(f"\n执行: {command[:80]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if show and out:
        print(out)
    if show and err:
        print("ERR:", err)
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("="*60)
print("快速修复后端路由")
print("="*60)

# 1. 检查后端代码是否有/api/animes路由
print("\n=== 1. 检查后端代码 ===")
out, err = run_command(ssh, "grep -n 'api/animes' /opt/anime-website/backend/server-simple.ts")
print(out)

# 2. 检查是否有健康检查路由
out, err = run_command(ssh, "grep -n 'api/health' /opt/anime-website/backend/server-simple.ts")
print("健康检查路由:", out)

# 3. 创建一个完整的后端代码
print("\n=== 2. 创建完整的后端代码 ===")
backend_code = """import express from 'express';
import cors from 'cors';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import mysql from 'mysql2/promise';

const app = express();
const PORT = 3001;
const JWT_SECRET = 'your-secret-key-change-in-production';

app.use(cors());
app.use(express.json());

const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

const pool = mysql.createPool(dbConfig);

async function testDbConnection() {
  try {
    const connection = await pool.getConnection();
    console.log('Successfully connected to MySQL database!');
    connection.release();
  } catch (error) {
    console.error('Failed to connect to MySQL database:', error);
  }
}

testDbConnection();

app.get('/api/health', (req, res) => {
  res.json({ success: true, message: '服务运行正常', data: null });
});

app.get('/api/animes', async (req, res) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const limit = parseInt(req.query.limit as string) || 10;
    const offset = (page - 1) * limit;

    const [animes] = await pool.execute(
      'SELECT * FROM animes ORDER BY id DESC LIMIT ? OFFSET ?',
      [limit, offset]
    ) as any[];

    const [countResult] = await pool.execute(
      'SELECT COUNT(*) as total FROM animes'
    ) as any[];
    const total = countResult[0].total;

    res.json({
      success: true,
      data: {
        animes,
        pagination: {
          page,
          limit,
          total,
          totalPages: Math.ceil(total / limit)
        }
      }
    });
  } catch (error) {
    console.error('获取动漫列表错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

app.get('/api/animes/:id', async (req, res) => {
  try {
    const animeId = parseInt(req.params.id);
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

app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
      return res.status(400).json({ success: false, message: '请填写完整信息' });
    }

    const [existingUsers] = await pool.execute(
      'SELECT id FROM users WHERE username = ? OR email = ?',
      [username, email]
    ) as any[];

    if (existingUsers.length > 0) {
      return res.status(400).json({ success: false, message: '用户名或邮箱已存在' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const [result] = await pool.execute(
      'INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, 0)',
      [username, email, hashedPassword]
    ) as any[];

    res.json({ success: true, message: '注册成功' });
  } catch (error) {
    console.error('注册错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

app.post('/api/auth/login', async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ success: false, message: '请填写用户名和密码' });
    }

    const [users] = await pool.execute(
      'SELECT * FROM users WHERE username = ?',
      [username]
    ) as any[];

    if (users.length === 0) {
      return res.status(401).json({ success: false, message: '用户名或密码错误' });
    }

    const user = users[0];
    const isValidPassword = await bcrypt.compare(password, user.password);

    if (!isValidPassword) {
      return res.status(401).json({ success: false, message: '用户名或密码错误' });
    }

    const token = jwt.sign(
      { id: user.id, username: user.username, isAdmin: user.is_admin },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.json({
      success: true,
      message: '登录成功',
      data: {
        token,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          isAdmin: user.is_admin
        }
      }
    });
  } catch (error) {
    console.error('登录错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

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

const isAdmin = (req: express.Request, res: express.Response, next: express.NextFunction) => {
  if (!(req as any).user.isAdmin) {
    return res.status(403).json({ success: false, message: '需要管理员权限' });
  }
  next();
};

app.get('/api/admin/animes', authenticateToken, isAdmin, async (req, res) => {
  try {
    const [animes] = await pool.execute('SELECT * FROM animes ORDER BY id DESC') as any[];
    res.json({ success: true, data: animes });
  } catch (error) {
    console.error('获取动漫列表错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

app.post('/api/admin/animes', authenticateToken, isAdmin, async (req, res) => {
  try {
    const { title, titleJp, description, coverImage, year, season, episodes, studio, genre, averageRating, ratingCount } = req.body;

    if (!title) {
      return res.status(400).json({ success: false, message: '动漫标题不能为空' });
    }

    const [result] = await pool.execute(
      'INSERT INTO animes (title, title_jp, description, cover_image, year, season, episodes, studio, genre, average_rating, rating_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [title, titleJp || '', description || '', coverImage || '', year || null, season || '', episodes || null, studio || '', genre || '', averageRating || 0, ratingCount || 0]
    ) as any[];

    const [newAnimes] = await pool.execute(
      'SELECT * FROM animes WHERE id = ?',
      [(result as any).insertId]
    ) as any[];

    res.json({
      success: true,
      message: '动漫添加成功',
      data: newAnimes[0]
    });
  } catch (error) {
    console.error('添加动漫错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

app.put('/api/admin/animes/:id', authenticateToken, isAdmin, async (req, res) => {
  try {
    const animeId = parseInt(req.params.id);
    const { title, titleJp, description, coverImage, year, season, episodes, studio, genre, averageRating, ratingCount } = req.body;

    const updateFields: string[] = [];
    const updateValues: any[] = [];

    if (title !== undefined) {
      updateFields.push('title = ?');
      updateValues.push(title);
    }
    if (titleJp !== undefined) {
      updateFields.push('title_jp = ?');
      updateValues.push(titleJp);
    }
    if (description !== undefined) {
      updateFields.push('description = ?');
      updateValues.push(description);
    }
    if (coverImage !== undefined) {
      updateFields.push('cover_image = ?');
      updateValues.push(coverImage);
    }
    if (year !== undefined) {
      updateFields.push('year = ?');
      updateValues.push(year);
    }
    if (season !== undefined) {
      updateFields.push('season = ?');
      updateValues.push(season);
    }
    if (episodes !== undefined) {
      updateFields.push('episodes = ?');
      updateValues.push(episodes);
    }
    if (studio !== undefined) {
      updateFields.push('studio = ?');
      updateValues.push(studio);
    }
    if (genre !== undefined) {
      updateFields.push('genre = ?');
      updateValues.push(genre);
    }
    if (averageRating !== undefined) {
      updateFields.push('average_rating = ?');
      updateValues.push(averageRating);
    }
    if (ratingCount !== undefined) {
      updateFields.push('rating_count = ?');
      updateValues.push(ratingCount);
    }

    if (updateFields.length === 0) {
      return res.status(400).json({ success: false, message: '没有要更新的内容' });
    }

    updateValues.push(animeId);

    await pool.execute(
      `UPDATE animes SET ${updateFields.join(', ')} WHERE id = ?`,
      updateValues
    );

    const [updatedAnimes] = await pool.execute(
      'SELECT * FROM animes WHERE id = ?',
      [animeId]
    ) as any[];

    res.json({
      success: true,
      message: '动漫信息更新成功',
      data: updatedAnimes[0]
    });
  } catch (error) {
    console.error('更新动漫错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

app.delete('/api/admin/animes/:id', authenticateToken, isAdmin, async (req, res) => {
  try {
    const animeId = parseInt(req.params.id);

    const [animes] = await pool.execute(
      'SELECT id, title FROM animes WHERE id = ?',
      [animeId]
    ) as any[];

    if (animes.length === 0) {
      return res.status(404).json({ success: false, message: '动漫不存在' });
    }

    await pool.execute('DELETE FROM ratings WHERE anime_id = ?', [animeId]);
    await pool.execute('DELETE FROM comments WHERE anime_id = ?', [animeId]);
    await pool.execute('DELETE FROM animes WHERE id = ?', [animeId]);

    res.json({
      success: true,
      message: `动漫「${animes[0].title}」删除成功`,
      data: null
    });
  } catch (error) {
    console.error('删除动漫错误:', error);
    res.status(500).json({ success: false, message: '服务器错误' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
"""

# 写入后端代码
run_command(ssh, f"cat > /opt/anime-website/backend/server-simple.ts <<'EOF'\n{backend_code}\nEOF")

# 4. 重启后端服务
print("\n=== 3. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend")
run_command(ssh, "sleep 3")

# 5. 测试API
print("\n=== 4. 测试API ===")
out, err = run_command(ssh, "curl -s http://localhost:3001/api/health 2>&1")
print("/api/health:", out)

out, err = run_command(ssh, "curl -s http://localhost:3001/api/animes?page=1&limit=5 2>&1")
print("/api/animes:", out[:500])

# 6. 检查PM2状态
print("\n=== 5. 检查PM2状态 ===")
out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
print(out)

ssh.close()

print("\n" + "="*60)
print("修复完成！")
print("请访问: http://59.110.214.50")
print("="*60)
