import mysql from 'mysql2/promise';
import * as readline from 'readline';

const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

// 创建命令行接口
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(query: string): Promise<string> {
  return new Promise(resolve => rl.question(query, resolve));
}

async function deleteFakeAnime() {
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    console.log('='.repeat(80));
    console.log('假动漫数据删除工具');
    console.log('='.repeat(80));
    
    // 1. 先统计数据
    const [countResult] = await connection.execute('SELECT COUNT(*) as total FROM animes');
    const totalCount = (countResult as any)[0].total;
    console.log(`\n当前总动漫数量: ${totalCount}`);
    
    // 2. 查找要删除的假数据
    console.log('\n正在查找假数据...');
    
    // 模式1: 标题中包含4位数字
    // 模式2: 标题中有多个空格分隔的数字
    const [toDelete] = await connection.execute(`
      SELECT id, title, title_jp, cover_image, studio, release_year
      FROM animes 
      WHERE title REGEXP '[0-9]{4}'
         OR title LIKE '% % % % %'
         OR (title_jp IS NULL OR title_jp = '')
      ORDER BY id ASC
      LIMIT 100
    `);
    
    const deleteCount = (toDelete as any[]).length;
    console.log(`\n找到前100条可能的假数据（共约${totalCount - 50}条可能需要删除）:`);
    
    (toDelete as any[]).slice(0, 20).forEach((anime, i) => {
      console.log(`${i + 1}. ID: ${anime.id} - ${anime.title}`);
    });
    
    if (deleteCount > 20) {
      console.log(`... 还有 ${deleteCount - 20} 条`);
    }
    
    // 3. 确认保留的真实数据
    console.log('\n' + '='.repeat(80));
    console.log('将保留的真实动漫（前10条）:');
    console.log('='.repeat(80));
    
    const [toKeep] = await connection.execute(`
      SELECT id, title, title_jp, cover_image, studio, release_year
      FROM animes 
      WHERE id >= 32000
         OR (title_jp IS NOT NULL AND title_jp != '')
      ORDER BY id DESC
      LIMIT 20
    `);
    
    (toKeep as any[]).slice(0, 10).forEach((anime, i) => {
      console.log(`${i + 1}. ID: ${anime.id} - ${anime.title}`);
      if (anime.title_jp) {
        console.log(`   日文: ${anime.title_jp}`);
      }
    });
    
    // 4. 询问用户确认
    console.log('\n' + '='.repeat(80));
    const answer = await question(
      `\n即将删除约 ${totalCount - 50} 条假数据，保留约 50+ 条真实动漫。\n` +
      `是否继续？(yes/no): `
    );
    
    if (answer.toLowerCase() !== 'yes' && answer.toLowerCase() !== 'y') {
      console.log('操作已取消。');
      rl.close();
      return;
    }
    
    // 5. 执行删除
    console.log('\n正在删除假数据...');
    
    // 保留ID较大的真实动漫和有日文标题的动漫
    const [deleteResult] = await connection.execute(`
      DELETE FROM animes 
      WHERE id < 32000
        AND (title REGEXP '[0-9]{4}'
             OR title LIKE '% % % % %'
             OR title_jp IS NULL
             OR title_jp = '')
    `);
    
    const deletedRows = (deleteResult as any).affectedRows;
    console.log(`\n✅ 成功删除 ${deletedRows} 条假数据！`);
    
    // 6. 查看删除后的结果
    const [newCountResult] = await connection.execute('SELECT COUNT(*) as total FROM animes');
    const newTotal = (newCountResult as any)[0].total;
    console.log(`\n删除后数据库中的动漫数量: ${newTotal}`);
    
    console.log('\n' + '='.repeat(80));
    console.log('删除后的动漫列表:');
    console.log('='.repeat(80));
    
    const [remaining] = await connection.execute(`
      SELECT id, title, title_jp, cover_image, studio, release_year
      FROM animes 
      ORDER BY id ASC
    `);
    
    (remaining as any[]).forEach((anime, i) => {
      console.log(`${i + 1}. ID: ${anime.id} - ${anime.title}`);
      if (anime.title_jp) {
        console.log(`   日文: ${anime.title_jp}`);
      }
    });
    
  } catch (error) {
    console.error('数据库错误:', error);
  } finally {
    await connection.end();
    rl.close();
    console.log('\n数据库连接已关闭');
  }
}

deleteFakeAnime();
