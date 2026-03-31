import mysql.connector
from mysql.connector import Error
import re

# 数据库连接配置
db_config = {
    'host': '59.110.214.50',
    'port': 3306,
    'user': 'anime_user',
    'password': 'Xinmima1109',
    'database': 'anime_db',
    'charset': 'utf8mb4'
}

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

def cleanup_title(title):
    """清理标题，去掉末尾的数字和奇怪的组合"""
    if not title:
        return title
    
    # 去掉末尾的数字（如 "战斗森林 1385" → "战斗森林"）
    title = re.sub(r'\s+\d+$', '', title)
    
    # 去掉像 "第X卷" 这样的后缀
    title = re.sub(r'\s+第\d+卷$', '', title)
    
    # 去掉括号内的数字
    title = re.sub(r'\s*\(\d+\)\s*$', '', title)
    title = re.sub(r'\s*（\d+）\s*$', '', title)
    
    return title.strip()

def is_anime_type(anime_type, description, title):
    """判断是否是动漫类型"""
    if not anime_type and not description and not title:
        return True  # 默认保留
    
    # 纪录片、综艺等关键词
    non_anime_keywords = [
        '纪录片', '纪实', '综艺', '真人秀', '访谈', '脱口秀',
        '新闻', '天气预报', '体育', '游戏直播', '电竞',
        'documentary', 'variety', 'reality', 'talk show',
        'news', 'sports', 'interview'
    ]
    
    # 检查是否包含非动漫关键词
    text = f"{anime_type or ''} {description or ''} {title or ''}".lower()
    
    for keyword in non_anime_keywords:
        if keyword.lower() in text:
            return False
    
    return True

def cleanup_database():
    connection = create_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        print("=" * 60)
        print("开始清理数据库...")
        print("=" * 60)
        
        # 1. 获取所有动漫数据
        cursor.execute("SELECT id, title, anime_type, description FROM animes ORDER BY id")
        all_animes = cursor.fetchall()
        print(f"\n当前数据库共有 {len(all_animes)} 条动漫数据")
        
        # 2. 识别要删除的数据
        to_delete = []
        to_update_title = []
        
        for anime in all_animes:
            anime_id = anime['id']
            title = anime['title'] or ''
            anime_type = anime['anime_type'] or ''
            description = anime['description'] or ''
            
            # 检查是否是"学者"
            if '学者' in title:
                print(f"  删除: ID={anime_id}, 标题='{title}' (包含'学者')")
                to_delete.append(anime_id)
                continue
            
            # 检查是否是非动漫类型
            if not is_anime_type(anime_type, description, title):
                print(f"  删除: ID={anime_id}, 标题='{title}' (非动漫类型)")
                to_delete.append(anime_id)
                continue
            
            # 检查标题是否需要清理
            cleaned_title = cleanup_title(title)
            if cleaned_title != title:
                print(f"  更新标题: ID={anime_id}, '{title}' → '{cleaned_title}'")
                to_update_title.append((anime_id, cleaned_title))
        
        # 3. 执行删除（分批处理，每次100条）
        if to_delete:
            print(f"\n准备删除 {len(to_delete)} 条数据...")
            batch_size = 100
            for i in range(0, len(to_delete), batch_size):
                batch = to_delete[i:i + batch_size]
                delete_sql = "DELETE FROM animes WHERE id IN (%s)" % ','.join(['%s'] * len(batch))
                cursor.execute(delete_sql, batch)
                connection.commit()
                print(f"  已删除批次 {i//batch_size + 1}, {len(batch)} 条")
            print(f"✓ 总共删除 {len(to_delete)} 条数据")
        
        # 4. 执行标题更新（分批处理）
        if to_update_title:
            print(f"\n准备更新 {len(to_update_title)} 条标题...")
            update_count = 0
            for anime_id, new_title in to_update_title:
                cursor.execute(
                    "UPDATE animes SET title = %s WHERE id = %s",
                    (new_title, anime_id)
                )
                update_count += 1
                if update_count % 100 == 0:
                    connection.commit()
                    print(f"  已更新 {update_count} 条标题...")
            
            connection.commit()
            print(f"✓ 已更新 {update_count} 条标题")
        
        # 5. 重新检查冷门佳作，确保只有200条
        print(f"\n检查冷门佳作数量...")
        cursor.execute("SELECT COUNT(*) as count FROM animes WHERE is_hidden_gem = 1")
        hidden_gems_count = cursor.fetchone()['count']
        print(f"当前冷门佳作数量: {hidden_gems_count}")
        
        if hidden_gems_count > 200:
            print(f"需要减少到200条，删除 {hidden_gems_count - 200} 条...")
            cursor.execute("""
                DELETE FROM animes 
                WHERE is_hidden_gem = 1 
                AND id NOT IN (
                    SELECT id FROM (
                        SELECT id FROM animes 
                        WHERE is_hidden_gem = 1 
                        ORDER BY average_rating DESC, rating_count DESC 
                        LIMIT 200
                    ) as temp
                )
            """)
            connection.commit()
            print(f"✓ 已调整冷门佳作数量")
        
        # 6. 最终统计
        cursor.execute("SELECT COUNT(*) as count FROM animes")
        final_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM animes WHERE is_hidden_gem = 1")
        final_hidden_gems = cursor.fetchone()['count']
        
        print("\n" + "=" * 60)
        print("清理完成!")
        print("=" * 60)
        print(f"最终数据库总量: {final_count} 条")
        print(f"冷门佳作数量: {final_hidden_gems} 条")
        print(f"删除数据量: {len(to_delete)} 条")
        print(f"更新标题量: {len(to_update_title)} 条")
        print("=" * 60)
        
        cursor.close()
        
    except Error as e:
        print(f"数据库错误: {e}")
        connection.rollback()
    finally:
        if connection.is_connected():
            connection.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    cleanup_database()
