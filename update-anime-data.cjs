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

// 示例动漫数据
const sampleAnimeData = [
  {
    title: '葬送的芙莉莲',
    title_jp: '葬送のフリーレン',
    description: '讲述了精灵魔法使芙莉莲与勇者一行人完成了打倒魔王的任务后，与勇者们各自回归了各自的生活，而芙莉莲则开始了新的旅程。',
    cover_image: 'https://picsum.photos/seed/frieren/300/400',
    episodes: 28,
    status: '已完结',
    release_year: 2024,
    release_date: '2024-01-05',
    studio: 'Madhouse',
    genre: '奇幻,冒险',
    average_rating: 9.2,
    rating_count: 120000,
    nationality: '日本',
    anime_type: '奇幻',
    is_movie: 0
  },
  {
    title: '迷宫饭 第二季',
    title_jp: 'ダンジョン飯 第2期',
    description: '继续讲述莱欧斯一行在迷宫中寻找被龙并吃掉各种魔物的冒险故事。',
    cover_image: 'https://picsum.photos/seed/dungeon2/300/400',
    episodes: 24,
    status: '已完结',
    release_year: 2025,
    release_date: '2025-01-10',
    studio: 'TRIGGER',
    genre: '奇幻,喜剧',
    average_rating: 8.9,
    rating_count: 95000,
    nationality: '日本',
    anime_type: '奇幻',
    is_movie: 0
  },
  {
    title: '药屋少女的呢喃 第二季',
    title_jp: '薬屋のひとりごと 第2期',
    description: '猫猫继续在后宫中用她的医学知识解决各种问题。',
    cover_image: 'https://picsum.photos/seed/kusuriya2/300/400',
    episodes: 26,
    status: '已完结',
    release_year: 2025,
    release_date: '2025-01-15',
    studio: 'TOHO animation',
    genre: '历史,悬疑',
    average_rating: 9.0,
    rating_count: 110000,
    nationality: '日本',
    anime_type: '悬疑',
    is_movie: 0
  },
  {
    title: '怪兽8号 第二季',
    title_jp: '怪獣8号 第2期',
    description: '日比野卡夫卡继续作为怪兽8号守护人类。',
    cover_image: 'https://picsum.photos/seed/kaiju2/300/400',
    episodes: 24,
    status: '已完结',
    release_year: 2025,
    release_date: '2025-01-20',
    studio: 'Production I.G',
    genre: '动作,科幻',
    average_rating: 8.7,
    rating_count: 85000,
    nationality: '日本',
    anime_type: '热血',
    is_movie: 0
  },
  {
    title: '我推的孩子 第二季',
    title_jp: '推しの子 第2期',
    description: '阿库亚和露比继续在娱乐圈中寻找真相。',
    cover_image: 'https://picsum.photos/seed/oshinoko2/300/400',
    episodes: 28,
    status: '已完结',
    release_year: 2025,
    release_date: '2025-02-01',
    studio: '动画工房',
    genre: '剧情,悬疑',
    average_rating: 8.8,
    rating_count: 98000,
    nationality: '日本',
    anime_type: '剧情',
    is_movie: 0
  }
];

async function checkAnimeExists(connection, title) {
  const [rows] = await connection.execute(
    'SELECT id FROM animes WHERE title = ?',
    [title]
  );
  return rows.length > 0;
}

async function insertOrUpdateAnime(connection, anime) {
  const exists = await checkAnimeExists(connection, anime.title);
  
  if (exists) {
    // 更新现有数据
    await connection.execute(`
      UPDATE animes 
      SET title_jp = ?, description = ?, cover_image = ?, 
          episodes = ?, status = ?, release_year = ?,
          release_date = ?, studio = ?, genre = ?,
          average_rating = ?, rating_count = ?, nationality = ?,
          anime_type = ?, is_movie = ?
      WHERE title = ?
    `, [
      anime.title_jp,
      anime.description,
      anime.cover_image,
      anime.episodes,
      anime.status,
      anime.release_year,
      anime.release_date,
      anime.studio,
      anime.genre,
      anime.average_rating,
      anime.rating_count,
      anime.nationality,
      anime.anime_type,
      anime.is_movie,
      anime.title
    ]);
    console.log(`✓ 更新动漫: ${anime.title}`);
  } else {
    // 插入新数据
    await connection.execute(`
      INSERT INTO animes 
      (title, title_jp, description, cover_image, episodes,
      status, release_year, release_date, studio, genre,
      average_rating, rating_count, nationality, anime_type, is_movie, created_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
    `, [
      anime.title,
      anime.title_jp,
      anime.description,
      anime.cover_image,
      anime.episodes,
      anime.status,
      anime.release_year,
      anime.release_date,
      anime.studio,
      anime.genre,
      anime.average_rating,
      anime.rating_count,
      anime.nationality,
      anime.anime_type,
      anime.is_movie
    ]);
    console.log(`✓ 添加新动漫: ${anime.title}`);
  }
}

async function main() {
  console.log('='.repeat(60));
  console.log('动漫数据获取和更新脚本');
  console.log('='.repeat(60));
  console.log();
  
  const connection = await mysql.createConnection(dbConfig);
  
  try {
    console.log(`获取到 ${sampleAnimeData.length} 条动漫数据`);
    console.log();
    
    let successCount = 0;
    
    for (const anime of sampleAnimeData) {
      await insertOrUpdateAnime(connection, anime);
      successCount++;
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    console.log();
    console.log('='.repeat(60));
    console.log(`更新完成！成功处理 ${successCount}/${sampleAnimeData.length} 条数据`);
    console.log('='.repeat(60));
    
  } catch (error) {
    console.error('发生错误:', error);
  } finally {
    await connection.end();
    console.log('数据库连接已关闭');
  }
}

main();
