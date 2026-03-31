const mysql = require('mysql2/promise');
const bcrypt = require('bcryptjs');

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
  console.log('='.repeat(60));
  console.log('重置数据库并设置管理员账号');
  console.log('='.repeat(60));
  console.log();
  
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    // 1. 清理用户表（保留必要数据）
    console.log('1. 清理用户表...');
    await connection.execute('DELETE FROM users WHERE username != "admin"');
    console.log('   ✓ 已清理非管理员用户');
    console.log();
    
    // 2. 检查 admin 用户是否存在
    console.log('2. 检查管理员账号...');
    const [adminUsers] = await connection.execute(
      'SELECT id FROM users WHERE username = ?',
      ['admin']
    );
    
    const adminPassword = 'Xinmima1109';
    const hashedPassword = await bcrypt.hash(adminPassword, 10);
    
    if (adminUsers.length === 0) {
      // 创建 admin 用户
      console.log('   创建管理员账号...');
      const avatar = 'https://picsum.photos/seed/admin/100/100';
      
      await connection.execute(`
        INSERT INTO users (username, email, password, avatar, created_at)
        VALUES (?, ?, ?, ?, NOW())
      `, ['admin', 'admin@example.com', hashedPassword, avatar]);
      
      console.log('   ✓ 管理员账号创建成功');
    } else {
      // 更新 admin 用户密码
      console.log('   更新管理员密码...');
      await connection.execute(
        'UPDATE users SET password = ? WHERE username = ?',
        [hashedPassword, 'admin']
      );
      console.log('   ✓ 管理员密码更新成功');
    }
    console.log();
    
    // 3. 清理其他相关表
    console.log('3. 清理评论和评分...');
    await connection.execute('DELETE FROM comments');
    await connection.execute('DELETE FROM ratings');
    console.log('   ✓ 已清理评论和评分');
    console.log();
    
    // 显示管理员账号信息
    console.log('='.repeat(60));
    console.log('管理员账号设置完成！');
    console.log('='.repeat(60));
    console.log();
    console.log('用户名: admin');
    console.log('密码: Xinmima1109');
    console.log();
    console.log('数据库重置完成！');
    console.log();
    
  } catch (error) {
    console.error('发生错误:', error);
  } finally {
    await connection.end();
  }
}

main();
