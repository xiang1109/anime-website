import mysql from 'mysql2/promise';

const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

async function checkRealAnime() {
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    console.log('='.repeat(80));
    console.log('查看高评分动漫（可能是真实数据）');
    console.log('='.repeat(80));
    
    // 查看评分9.0以上的动漫
    const [highRated] = await connection.execute(`
      SELECT id, title, title_jp, cover_image, studio, release_year, 
             average_rating, rating_count, description
      FROM animes 
      WHERE average_rating >= 9.0
      ORDER BY average_rating DESC, rating_count DESC
      LIMIT 50
    `);
    
    console.log(`\n找到 ${(highRated as any[]).length} 条评分9.0以上的动漫:`);
    (highRated as any[]).forEach((anime, i) => {
      console.log(`\n${i + 1}. ID: ${anime.id}`);
      console.log(`   标题: ${anime.title}`);
      if (anime.title_jp) {
        console.log(`   日文: ${anime.title_jp}`);
      }
      console.log(`   评分: ${anime.average_rating} (${anime.rating_count}人)`);
      console.log(`   工作室: ${anime.studio}`);
      console.log(`   年份: ${anime.release_year}`);
      if (anime.description) {
        console.log(`   描述: ${anime.description.substring(0, 80)}...`);
      }
    });
    
    // 查看ID较大的动漫
    console.log('\n' + '='.repeat(80));
    console.log('查看ID较大的动漫（可能是后来添加的真实数据）');
    console.log('='.repeat(80));
    
    const [highId] = await connection.execute(`
      SELECT id, title, title_jp, cover_image, studio, release_year, 
             average_rating, rating_count, description
      FROM animes 
      ORDER BY id DESC
      LIMIT 50
    `);
    
    console.log(`\nID最大的50条动漫:`);
    (highId as any[]).forEach((anime, i) => {
      console.log(`${i + 1}. ID: ${anime.id} - ${anime.title}`);
    });
    
  } catch (error) {
    console.error('数据库错误:', error);
  } finally {
    await connection.end();
    console.log('\n数据库连接已关闭');
  }
}

checkRealAnime();
