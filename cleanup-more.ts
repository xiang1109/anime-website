import mysql from 'mysql2/promise';

const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

async function cleanupMore() {
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    console.log('='.repeat(80));
    console.log('进一步清理假数据...');
    console.log('='.repeat(80));
    
    // 删除ID 32000-32024的假数据，只保留有日文标题或真实国产动漫
    const [deleteResult] = await connection.execute(`
      DELETE FROM animes 
      WHERE id >= 32000 AND id <= 32024
        AND (title_jp IS NULL OR title_jp = '')
        AND title NOT IN ('中国奇谭', '雾山五行', '大理寺日志', '时光代理人', '罗小黑战记', '刺客伍六七')
    `);
    
    const deletedRows = (deleteResult as any).affectedRows;
    console.log(`\n✅ 再次删除 ${deletedRows} 条假数据！`);
    
    // 查看最终结果
    const [finalCount] = await connection.execute('SELECT COUNT(*) as total FROM animes');
    const finalTotal = (finalCount as any)[0].total;
    console.log(`\n最终数据库中的动漫数量: ${finalTotal}`);
    
    console.log('\n' + '='.repeat(80));
    console.log('最终保留的动漫列表:');
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
    
  } catch (error) {
    console.error('数据库错误:', error);
  } finally {
    await connection.end();
    console.log('\n数据库连接已关闭');
  }
}

cleanupMore();
