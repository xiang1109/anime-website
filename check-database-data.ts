import mysql from 'mysql2/promise';

const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

async function checkDatabase() {
  console.log('🔍 正在连接数据库...\n');
  
  let connection;
  try {
    connection = await mysql.createConnection(dbConfig);
    console.log('✅ 数据库连接成功！\n');

    // 检查动漫表
    const [animeCount] = await connection.execute('SELECT COUNT(*) as count FROM animes');
    console.log(`📊 动漫表总数: ${(animeCount as any)[0].count} 条\n`);

    // 查看前20条数据
    console.log('🎬 前20条动漫数据:');
    console.log('='.repeat(100));
    
    const [animes] = await connection.execute(`
      SELECT id, title, title_jp, release_year, status, studio, average_rating, rating_count 
      FROM animes 
      ORDER BY id DESC 
      LIMIT 20
    `);
    
    (animes as any[]).forEach((anime, index) => {
      console.log(`${index + 1}. [ID:${anime.id}] ${anime.title || '无标题'} ${anime.title_jp ? `(${anime.title_jp})` : ''}`);
      console.log(`   年份: ${anime.release_year || 'N/A'} | 状态: ${anime.status || 'N/A'} | 工作室: ${anime.studio || 'N/A'}`);
      console.log(`   评分: ${anime.average_rating || 'N/A'} (${anime.rating_count || 0}条评价)`);
      console.log('-' . repeat(100));
    });

    // 检查用户表
    const [userCount] = await connection.execute('SELECT COUNT(*) as count FROM users');
    console.log(`\n👥 用户表总数: ${(userCount as any)[0].count} 条\n`);

    // 检查评论表
    const [commentCount] = await connection.execute('SELECT COUNT(*) as count FROM comments');
    console.log(`💬 评论表总数: ${(commentCount as any)[0].count} 条\n`);

    // 获取统计信息
    console.log('📈 数据统计:');
    console.log('-'.repeat(50));
    
    const [statusStats] = await connection.execute(`
      SELECT status, COUNT(*) as count 
      FROM animes 
      GROUP BY status
    `);
    console.log('状态分布:');
    (statusStats as any[]).forEach(stat => {
      console.log(`  ${stat.status || '未知'}: ${stat.count} 部`);
    });

    const [yearStats] = await connection.execute(`
      SELECT release_year, COUNT(*) as count 
      FROM animes 
      WHERE release_year IS NOT NULL 
      GROUP BY release_year 
      ORDER BY release_year DESC 
      LIMIT 10
    `);
    console.log('\n年份分布 (TOP 10):');
    (yearStats as any[]).forEach(stat => {
      console.log(`  ${stat.release_year}年: ${stat.count} 部`);
    });

    const [studioStats] = await connection.execute(`
      SELECT studio, COUNT(*) as count 
      FROM animes 
      WHERE studio IS NOT NULL AND studio != ''
      GROUP BY studio 
      ORDER BY count DESC 
      LIMIT 10
    `);
    console.log('\n工作室分布 (TOP 10):');
    (studioStats as any[]).forEach(stat => {
      console.log(`  ${stat.studio}: ${stat.count} 部`);
    });

  } catch (error) {
    console.error('❌ 检查数据库时出错:', error);
  } finally {
    if (connection) {
      await connection.end();
      console.log('\n👋 数据库连接已关闭');
    }
  }
}

checkDatabase();
