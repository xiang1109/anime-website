import mysql from 'mysql2/promise';

const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

async function deleteFakeAnime() {
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    console.log('='.repeat(80));
    console.log('开始删除假动漫数据...');
    console.log('='.repeat(80));
    
    // 1. 先统计数据
    const [countResult] = await connection.execute('SELECT COUNT(*) as total FROM animes');
    const totalCount = (countResult as any)[0].total;
    console.log(`\n删除前总动漫数量: ${totalCount}`);
    
    // 2. 执行删除
    console.log('\n正在删除假数据...');
    
    // 删除策略：
    // - 保留 ID >= 32000 的动漫（真实数据）
    // - 保留有日文标题的动漫
    // - 删除其他的
    const [deleteResult] = await connection.execute(`
      DELETE FROM animes 
      WHERE id < 32000
        AND (title_jp IS NULL OR title_jp = '')
    `);
    
    const deletedRows = (deleteResult as any).affectedRows;
    console.log(`\n✅ 成功删除 ${deletedRows} 条假数据！`);
    
    // 3. 查看删除后的结果
    const [newCountResult] = await connection.execute('SELECT COUNT(*) as total FROM animes');
    const newTotal = (newCountResult as any)[0].total;
    console.log(`\n删除后数据库中的动漫数量: ${newTotal}`);
    
    console.log('\n' + '='.repeat(80));
    console.log('保留的动漫列表:');
    console.log('='.repeat(80));
    
    const [remaining] = await connection.execute(`
      SELECT id, title, title_jp, cover_image, studio, release_year, average_rating
      FROM animes 
      ORDER BY id ASC
    `);
    
    (remaining as any[]).forEach((anime, i) => {
      console.log(`\n${i + 1}. ID: ${anime.id}`);
      console.log(`   标题: ${anime.title}`);
      if (anime.title_jp) {
        console.log(`   日文: ${anime.title_jp}`);
      }
      console.log(`   评分: ${anime.average_rating}`);
      console.log(`   工作室: ${anime.studio}`);
      console.log(`   年份: ${anime.release_year}`);
    });
    
    console.log('\n' + '='.repeat(80));
    console.log('✅ 删除完成！');
    console.log('='.repeat(80));
    
  } catch (error) {
    console.error('数据库错误:', error);
  } finally {
    await connection.end();
    console.log('\n数据库连接已关闭');
  }
}

deleteFakeAnime();
