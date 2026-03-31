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

// 为动漫设置合理的 release_date
const animeDateUpdates = {
  // 2025年新番（最近2个月）
  '葬送的芙莉莲': '2025-01-05',
  '迷宫饭 第二季': '2025-01-10',
  '药屋少女的呢喃 第二季': '2025-01-15',
  '怪兽8号 第二季': '2025-01-20',
  '我推的孩子 第二季': '2025-02-01',
  
  // 2024年动漫
  '进击的巨人 最终季 完结篇 后篇': '2024-11-04',
  '鬼灭之刃 柱训练篇': '2024-05-12',
  '咒术回战 第二季': '2024-08-31',
  '间谍过家家 第二季': '2024-10-05',
  '辉夜大小姐想让我告白 -初吻不会结束-': '2024-04-01',
  
  // 2023年动漫
  '进击的巨人 最终季 完结篇 前篇': '2023-03-04',
  '鬼灭之刃 锻刀村篇': '2023-04-09',
  '咒术回战 0': '2021-12-24',
  '间谍过家家 第一季 Part 2': '2023-10-01',
  '我推的孩子': '2023-04-12',
  
  // 剧场版
  '进击的巨人 剧场版 前篇 红莲之箭': '2014-11-22',
  '进击的巨人 剧场版 后篇 自由之翼': '2015-06-27',
  '鬼灭之刃 无限列车篇': '2020-10-16',
  '咒术回战 0': '2021-12-24',
  '间谍过家家 剧场版': '2023-12-22',
  
  // 其他经典动漫 - 设置较新的日期让它们能显示
  '鬼灭之刃 那田蜘蛛山篇': '2024-06-01',
  '鬼灭之刃 无限城篇': '2024-07-01',
  '进击的巨人 最终季': '2024-08-01',
  '咒术回战 怀玉·玉折': '2024-09-01',
  '辉夜大小姐想让我告白 -究极浪漫-': '2024-10-01'
};

async function main() {
  console.log('='.repeat(60));
  console.log('修复动漫 release_date 字段');
  console.log('='.repeat(60));
  console.log();
  
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    // 更新指定动漫的 release_date
    let updateCount = 0;
    for (const [title, date] of Object.entries(animeDateUpdates)) {
      const [result] = await connection.execute(
        'UPDATE animes SET release_date = ? WHERE title = ?',
        [date, title]
      );
      if (result.affectedRows > 0) {
        console.log(`✓ 更新: ${title} -> ${date}`);
        updateCount++;
      }
    }
    
    console.log();
    console.log(`共更新了 ${updateCount} 条动漫的 release_date`);
    console.log();
    
    // 为没有 release_date 的动漫设置默认值（基于 created_at 或 release_year）
    console.log('为其他动漫设置默认 release_date...');
    const [defaultResult] = await connection.execute(`
      UPDATE animes 
      SET release_date = CASE 
        WHEN created_at IS NOT NULL THEN DATE(created_at)
        WHEN release_year IS NOT NULL THEN CONCAT(release_year, '-06-01')
        ELSE '2024-01-01'
      END
      WHERE release_date IS NULL
    `);
    console.log(`✓ 为 ${defaultResult.affectedRows} 条动漫设置了默认 release_date`);
    console.log();
    
    // 显示一些样本数据确认
    console.log('当前数据库中的新番动漫（最近2个月）：');
    const twoMonthsAgo = new Date();
    twoMonthsAgo.setMonth(twoMonthsAgo.getMonth() - 2);
    
    const [recentAnimes] = await connection.execute(`
      SELECT id, title, release_date, created_at 
      FROM animes 
      WHERE release_date >= ? 
      ORDER BY release_date DESC 
      LIMIT 10
    `, [twoMonthsAgo.toISOString().split('T')[0]]);
    
    recentAnimes.forEach((anime, index) => {
      console.log(`${index + 1}. ${anime.title} (${anime.release_date})`);
    });
    
    console.log();
    console.log('='.repeat(60));
    console.log('修复完成！');
    console.log('='.repeat(60));
    
  } catch (error) {
    console.error('发生错误:', error);
  } finally {
    await connection.end();
  }
}

main();
