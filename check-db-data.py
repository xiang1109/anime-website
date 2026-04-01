import pymysql
import sys

print('🔍 正在连接数据库...\n')

try:
    connection = pymysql.connect(
        host='59.110.214.50',
        port=3306,
        user='anime_user',
        password='Xinmima1109',
        database='anime_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print('✅ 数据库连接成功！\n')

    with connection.cursor() as cursor:
        # 检查动漫表
        cursor.execute('SELECT COUNT(*) as count FROM animes')
        anime_count = cursor.fetchone()
        print(f'📊 动漫表总数: {anime_count["count"]} 条\n')

        # 查看前20条数据
        print('🎬 前20条动漫数据:')
        print('=' * 100)
        
        cursor.execute('''
            SELECT id, title, title_jp, release_year, status, studio, 
                   average_rating, rating_count, nationality
            FROM animes 
            ORDER BY id DESC 
            LIMIT 20
        ''')
        animes = cursor.fetchall()
        
        for idx, anime in enumerate(animes, 1):
            title = anime['title'] or '无标题'
            title_jp = f' ({anime["title_jp"]})' if anime['title_jp'] else ''
            year = anime['release_year'] or 'N/A'
            status = anime['status'] or 'N/A'
            studio = anime['studio'] or 'N/A'
            rating = anime['average_rating'] or 'N/A'
            rating_count = anime['rating_count'] or 0
            nationality = anime['nationality'] or 'N/A'
            
            print(f'{idx}. [ID:{anime["id"]}] {title}{title_jp}')
            print(f'   年份: {year} | 状态: {status} | 工作室: {studio} | 国籍: {nationality}')
            print(f'   评分: {rating} ({rating_count}条评价)')
            print('-' * 100)

        # 检查用户表
        cursor.execute('SELECT COUNT(*) as count FROM users')
        user_count = cursor.fetchone()
        print(f'\n👥 用户表总数: {user_count["count"]} 条\n')

        # 检查评论表
        cursor.execute('SELECT COUNT(*) as count FROM comments')
        comment_count = cursor.fetchone()
        print(f'💬 评论表总数: {comment_count["count"]} 条\n')

        # 获取统计信息
        print('📈 数据统计:')
        print('-' * 50)
        
        # 状态分布
        cursor.execute('SELECT status, COUNT(*) as count FROM animes GROUP BY status')
        status_stats = cursor.fetchall()
        print('状态分布:')
        for stat in status_stats:
            status_name = stat['status'] or '未知'
            print(f'  {status_name}: {stat["count"]} 部')

        # 年份分布
        cursor.execute('''
            SELECT release_year, COUNT(*) as count 
            FROM animes 
            WHERE release_year IS NOT NULL 
            GROUP BY release_year 
            ORDER BY release_year DESC 
            LIMIT 10
        ''')
        year_stats = cursor.fetchall()
        print('\n年份分布 (TOP 10):')
        for stat in year_stats:
            print(f'  {stat["release_year"]}年: {stat["count"]} 部')

        # 工作室分布
        cursor.execute('''
            SELECT studio, COUNT(*) as count 
            FROM animes 
            WHERE studio IS NOT NULL AND studio != ''
            GROUP BY studio 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        studio_stats = cursor.fetchall()
        print('\n工作室分布 (TOP 10):')
        for stat in studio_stats:
            print(f'  {stat["studio"]}: {stat["count"]} 部')

        # 国籍分布
        cursor.execute('''
            SELECT nationality, COUNT(*) as count 
            FROM animes 
            WHERE nationality IS NOT NULL AND nationality != ''
            GROUP BY nationality 
            ORDER BY count DESC
        ''')
        nationality_stats = cursor.fetchall()
        print('\n国籍分布:')
        for stat in nationality_stats:
            print(f'  {stat["nationality"]}: {stat["count"]} 部')

    connection.close()
    print('\n👋 数据库连接已关闭')

except Exception as e:
    print(f'❌ 检查数据库时出错: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
