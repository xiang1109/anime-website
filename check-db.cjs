const mysql = require('mysql2/promise');

const dbConfig = {
  host: '59.110.214.50',
  port: 3306,
  user: 'anime_user',
  password: 'Xinmima1109',
  database: 'anime_db',
  charset: 'utf8mb4'
};

async function checkDatabase() {
  try {
    const connection = await mysql.createConnection(dbConfig);
    console.log('数据库连接成功！\n');

    // 查看所有表
    const [tables] = await connection.execute('SHOW TABLES');
    console.log('数据库中的表：');
    tables.forEach(table => {
      console.log('  -', Object.values(table)[0]);
    });
    console.log('\n');

    // 查看 animes 表结构
    console.log('=== animes 表结构 ===');
    const [columns] = await connection.execute('DESCRIBE animes');
    columns.forEach(col => {
      console.log(`${col.Field}: ${col.Type} ${col.Null === 'YES' ? 'NULL' : 'NOT NULL'} ${col.Default ? 'DEFAULT ' + col.Default : ''}`);
    });
    console.log('\n');

    // 查看一些样本数据
    console.log('=== 样本数据（前5条） ===');
    const [rows] = await connection.execute('SELECT * FROM animes LIMIT 5');
    rows.forEach((row, index) => {
      console.log(`\n动漫 ${index + 1}:`);
      Object.entries(row).forEach(([key, value]) => {
        console.log(`  ${key}: ${value}`);
      });
    });

    await connection.end();
  } catch (error) {
    console.error('错误：', error);
  }
}

checkDatabase();
