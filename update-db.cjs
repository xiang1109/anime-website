const mysql = require('mysql2/promise');

const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

async function updateDatabase() {
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    console.log('开始更新数据库...\n');

    // 检查 release_date 字段是否存在
    const [columns] = await connection.execute('DESCRIBE animes');
    const hasReleaseDate = columns.some(col => col.Field === 'release_date');

    if (!hasReleaseDate) {
      console.log('添加 release_date 字段...');
      await connection.execute(`
        ALTER TABLE animes 
        ADD COLUMN release_date DATE NULL 
        AFTER release_year
      `);
      console.log('✓ release_date 字段添加成功\n');
    } else {
      console.log('✓ release_date 字段已存在\n');
    }

    // 为现有数据填充 release_date（如果 release_year 存在）
    console.log('更新现有数据的 release_date...');
    const [updateResult] = await connection.execute(`
      UPDATE animes 
      SET release_date = CONCAT(release_year, '-01-01') 
      WHERE release_year IS NOT NULL 
        AND release_date IS NULL
    `);
    console.log(`✓ 更新了 ${updateResult.affectedRows} 条记录\n`);

    console.log('数据库更新完成！');
    
  } catch (error) {
    console.error('更新失败：', error);
  } finally {
    await connection.end();
  }
}

updateDatabase();
