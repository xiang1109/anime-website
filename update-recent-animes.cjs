const mysql = require('mysql2/promise');

// 数据库配置
const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

// 为最近2个月（2026年1-3月）的动漫设置合理的日期
const recentAnimeUpdates = {
  // 2026年1月新番
  '葬送的芙莉莲 特别篇': '2026-01-08',
  '迷宫饭 第三季': '2026-01-10',
  '药屋少女的呢喃 第三季': '2026-01-12',
  
  // 2026年2月新番
  '怪兽8号 第三季': '2026-02-05',
  '我推的孩子 第三季': '2026-02-07',
  '间谍过家家 第三季': '2026-02-14',
  
  // 2026年3月新番（最近）
  '鬼灭之刃 无限城篇 后篇': '2026-03-01',
  '进击的巨人 特别篇': '2026-03-08',
  '咒术回战 第三季': '2026-03-15',
  '辉夜大小姐想让我告白 第四季': '2026-03-20',
  
  // 已有的动漫更新日期
  '葬送的芙莉莲': '2026-01-05',
  '迷宫饭 第二季': '2026-01-15',
  '药屋少女的呢喃 第二季': '2026-02-01',
  '怪兽8号 第二季': '2026-02-15',
  '我推的孩子 第二季': '2026-03-01'
};

async function main() {
  console.log('='.repeat(60));
  console.log('更新最近2个月的动漫');
  console.log('='.repeat(60));
  console.log();
  
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    // 更新动漫的 release_date
    let updateCount = 0;
    for (const [title, date] of Object.entries(recentAnimeUpdates)) {
      // 先检查动漫是否存在
      const [existing] = await connection.execute(
        'SELECT id FROM animes WHERE title = ?',
        [title]
      );
      
      if (existing.length > 0) {
        // 更新现有动漫
        await connection.execute(
          'UPDATE animes SET release_date = ? WHERE title = ?',
          [date, title]
        );
        console.log(`✓ 更新: ${title} -> ${date}`);
        updateCount++;
      } else {
        // 如果不存在，插入新动漫（简化版本）
        await connection.execute(`
          INSERT INTO animes 
          (title, description, cover_image, episodes, status, 
           release_year, release_date, studio, genre, 
           average_rating, rating_count, nationality, anime_type, is_movie, created_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
        `, [
          title,
          `${title}的精彩故事`,
          `https://picsum.photos/seed/${encodeURIComponent(title)}/300/400`,
          12,
          '已完结',
          parseInt(date.split('-')[0]),
          date,
          '知名动画公司',
          '动画',
          8.5,
          50000,
          '日本',
          '动画',
          0
        ]);
        console.log(`✓ 新增: ${title} -> ${date}`);
        updateCount++;
      }
    }
    
    console.log();
    console.log(`共处理了 ${updateCount} 条动漫`);
    console.log();
    
    // 显示当前数据库中的新番动漫
    console.log('当前数据库中的新番动漫（最近2个月）：');
    const twoMonthsAgo = new Date();
    twoMonthsAgo.setMonth(twoMonthsAgo.getMonth() - 2);
    
    const [recentAnimes] = await connection.execute(`
      SELECT id, title, release_date 
      FROM animes 
      WHERE release_date >= ? 
      ORDER BY release_date DESC 
      LIMIT 15
    `, [twoMonthsAgo.toISOString().split('T')[0]]);
    
    recentAnimes.forEach((anime, index) => {
      console.log(`${index + 1}. ${anime.title} (${anime.release_date})`);
    });
    
    console.log();
    console.log('='.repeat(60));
    console.log('更新完成！');
    console.log('='.repeat(60));
    
  } catch (error) {
    console.error('发生错误:', error);
  } finally {
    await connection.end();
  }
}

main();
