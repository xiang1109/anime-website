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
    
    # 去掉重复数字，如 "XXX 413 413" → "XXX 413"
    title = re.sub(r'(\s+\d+)\1+$', r'\1', title)
    
    return title.strip()

def simple_cleanup():
    connection = create_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        print("=" * 60)
        print("开始简单清理数据库...")
        print("=" * 60)
        
        # 1. 获取所有动漫数据
        cursor.execute("SELECT id, title FROM animes ORDER BY id")
        all_animes = cursor.fetchall()
        print(f"\n当前数据库共有 {len(all_animes)} 条动漫数据")
        
        # 2. 更新标题
        to_update = []
        for anime in all_animes:
            anime_id = anime['id']
            title = anime['title'] or ''
            
            cleaned_title = cleanup_title(title)
            if cleaned_title != title:
                to_update.append((anime_id, cleaned_title))
        
        if to_update:
            print(f"\n准备更新 {len(to_update)} 条标题...")
            update_count = 0
            for anime_id, new_title in to_update:
                cursor.execute(
                    "UPDATE animes SET title = %s WHERE id = %s",
                    (new_title, anime_id)
                )
                update_count += 1
                if update_count % 50 == 0:
                    connection.commit()
                    print(f"  已更新 {update_count} 条标题...")
            
            connection.commit()
            print(f"✓ 已更新 {update_count} 条标题")
        
        # 3. 确保冷门佳作有200条
        print(f"\n检查冷门佳作数量...")
        cursor.execute("SELECT COUNT(*) as count FROM animes WHERE is_hidden_gem = 1")
        hidden_gems_count = cursor.fetchone()['count']
        print(f"当前冷门佳作数量: {hidden_gems_count}")
        
        if hidden_gems_count < 200:
            print(f"需要增加到200条，补充 {200 - hidden_gems_count} 条...")
            # 选择高分的动漫设置为冷门佳作
            cursor.execute("""
                UPDATE animes 
                SET is_hidden_gem = 1 
                WHERE is_hidden_gem = 0 
                ORDER BY average_rating DESC, rating_count DESC 
                LIMIT %s
            """, (200 - hidden_gems_count,))
            connection.commit()
            print(f"✓ 已补充冷门佳作")
        elif hidden_gems_count > 200:
            print(f"需要减少到200条，删除 {hidden_gems_count - 200} 条...")
            cursor.execute("""
                UPDATE animes 
                SET is_hidden_gem = 0 
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
        
        # 4. 最终统计
        cursor.execute("SELECT COUNT(*) as count FROM animes")
        final_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM animes WHERE is_hidden_gem = 1")
        final_hidden_gems = cursor.fetchone()['count']
        
        print("\n" + "=" * 60)
        print("清理完成!")
        print("=" * 60)
        print(f"最终数据库总量: {final_count} 条")
        print(f"冷门佳作数量: {final_hidden_gems} 条")
        print(f"更新标题量: {len(to_update)} 条")
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
    simple_cleanup()
