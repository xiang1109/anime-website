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

async function main() {
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    console.log('='.repeat(60));
    console.log('检查动漫状态分布');
    console.log('='.repeat(60));
    console.log();
    
    // 统计各状态的动漫数量
    const [statusStats] = await connection.execute(`
      SELECT status, COUNT(*) as count 
      FROM animes 
      GROUP BY status
    `);
    
    console.log('动漫状态统计：');
    statusStats.forEach(stat => {
      console.log(`  ${stat.status || 'NULL'}: ${stat.count} 部`);
    });
    console.log();
    
    // 如果连载动漫太少，更新一些动漫为连载中
    if (statusStats.find(s => s.status === '连载中')?.count < 5) {
      console.log('连载动漫较少，正在更新一些动漫为连载中...');
      
      // 更新一些热门动漫为连载中
      const titlesToUpdate = [
        '海贼王',
        '进击的巨人',
        '鬼灭之刃',
        '咒术回战',
        '间谍过家家'
      ];
      
      let updateCount = 0;
      for (const title of titlesToUpdate) {
        const [result] = await connection.execute(
          "UPDATE animes SET status = '连载中' WHERE title = ?",
          [title]
        );
        if (result.affectedRows > 0) {
          console.log(`  ✓ 更新: ${title}`);
          updateCount++;
        }
      }
      console.log(`共更新了 ${updateCount} 部动漫为连载中\n`);
    }
    
    // 显示各分类的前3部动漫
    console.log('各分类示例动漫：');
    console.log();
    
    // 新番动漫
    console.log('【新番动漫】');
    const twoMonthsAgo = new Date();
    twoMonthsAgo.setMonth(twoMonthsAgo.getMonth() - 2);
    const [recentAnimes] = await connection.execute(`
      SELECT title, average_rating, rating_count, release_date 
      FROM animes 
      WHERE release_date >= ? 
      ORDER BY average_rating DESC, rating_count DESC 
      LIMIT 3
    `, [twoMonthsAgo.toISOString().split('T')[0]]);
    recentAnimes.forEach((anime, i) => {
      console.log(`  ${i + 1}. ${anime.title} (评分: ${anime.average_rating}, 评论: ${anime.rating_count})`);
    });
    console.log();
    
    // 连载动漫
    console.log('【连载动漫】');
    const [ongoingAnimes] = await connection.execute(`
      SELECT title, average_rating, rating_count 
      FROM animes 
      WHERE status = '连载中' 
      ORDER BY average_rating DESC, rating_count DESC 
      LIMIT 3
    `);
    ongoingAnimes.forEach((anime, i) => {
      console.log(`  ${i + 1}. ${anime.title} (评分: ${anime.average_rating}, 评论: ${anime.rating_count})`);
    });
    console.log();
    
    // 完结动漫
    console.log('【完结动漫】');
    const [completedAnimes] = await connection.execute(`
      SELECT title, average_rating, rating_count 
      FROM animes 
      WHERE status = '已完结' 
      ORDER BY average_rating DESC, rating_count DESC 
      LIMIT 3
    `);
    completedAnimes.forEach((anime, i) => {
      console.log(`  ${i + 1}. ${anime.title} (评分: ${anime.average_rating}, 评论: ${anime.rating_count})`);
    });
    console.log();
    
    // 剧场版
    console.log('【剧场版】');
    const [theaterAnimes] = await connection.execute(`
      SELECT title, average_rating, rating_count 
      FROM animes 
      WHERE is_movie = 1 
      ORDER BY average_rating DESC, rating_count DESC 
      LIMIT 3
    `);
    theaterAnimes.forEach((anime, i) => {
      console.log(`  ${i + 1}. ${anime.title} (评分: ${anime.average_rating}, 评论: ${anime.rating_count})`);
    });
    console.log();
    
    console.log('='.repeat(60));
    console.log('检查完成！所有列表都按评分降序，评分相同按评论量排序');
    console.log('='.repeat(60));
    
  } catch (error) {
    console.error('发生错误:', error);
  } finally {
    await connection.end();
  }
}

main();
