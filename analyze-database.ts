import mysql from 'mysql2/promise';

const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

async function analyzeDatabase() {
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    console.log('='.repeat(80));
    console.log('数据库数据分析');
    console.log('='.repeat(80));
    
    // 1. 获取总数据量
    const [countResult] = await connection.execute('SELECT COUNT(*) as total FROM animes');
    const totalCount = (countResult as any)[0].total;
    console.log(`\n总动漫数量: ${totalCount}`);
    
    // 2. 获取前50条数据查看
    console.log('\n' + '='.repeat(80));
    console.log('前50条动漫数据样本:');
    console.log('='.repeat(80));
    
    const [animes] = await connection.execute(`
      SELECT id, title, title_jp, cover_image, studio, release_year, description
      FROM animes 
      LIMIT 50
    `);
    
    (animes as any[]).forEach((anime, i) => {
      console.log(`\n${i + 1}. ID: ${anime.id}`);
      console.log(`   标题: ${anime.title}`);
      if (anime.title_jp) {
        console.log(`   日文标题: ${anime.title_jp}`);
      }
      console.log(`   封面: ${anime.cover_image}`);
      console.log(`   工作室: ${anime.studio}`);
      console.log(`   年份: ${anime.release_year}`);
    });
    
    // 3. 查找可疑数据
    console.log('\n' + '='.repeat(80));
    console.log('查找可疑数据:');
    console.log('='.repeat(80));
    
    // 查找标题中有多个数字的
    const [suspicious] = await connection.execute(`
      SELECT id, title, title_jp, cover_image 
      FROM animes 
      WHERE title REGEXP '[0-9]{4}'
         OR title LIKE '% % % % %'
      LIMIT 30
    `);
    
    console.log(`\n找到 ${(suspicious as any[]).length} 条可能有问题的数据:`);
    (suspicious as any[]).forEach((anime, i) => {
      console.log(`${i + 1}. ID: ${anime.id} - 标题: ${anime.title}`);
    });
    
    // 4. 工作室统计
    console.log('\n' + '='.repeat(80));
    console.log('工作室统计 (前20):');
    console.log('='.repeat(80));
    
    const [studios] = await connection.execute(`
      SELECT studio, COUNT(*) as count 
      FROM animes 
      GROUP BY studio 
      ORDER BY count DESC 
      LIMIT 20
    `);
    
    (studios as any[]).forEach((s) => {
      console.log(`${s.studio}: ${s.count}`);
    });
    
  } catch (error) {
    console.error('数据库错误:', error);
  } finally {
    await connection.end();
    console.log('\n数据库连接已关闭');
  }
}

analyzeDatabase();
