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

def analyze_data():
    connection = create_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        print("=" * 80)
        print("数据库数据分析")
        print("=" * 80)
        
        # 1. 获取总数据量
        cursor.execute("SELECT COUNT(*) as total FROM animes")
        total_count = cursor.fetchone()['total']
        print(f"\n总动漫数量: {total_count}")
        
        # 2. 分析标题模式
        print("\n" + "=" * 80)
        print("标题模式分析:")
        print("=" * 80)
        
        # 检查标题中包含数字的模式
        cursor.execute("""
            SELECT id, title, title_jp, cover_image, studio, release_year, description
            FROM animes 
            LIMIT 50
        """)
        animes = cursor.fetchall()
        
        print("\n前50条动漫数据样本:")
        for i, anime in enumerate(animes, 1):
            print(f"\n{i}. ID: {anime['id']}")
            print(f"   标题: {anime['title']}")
            if anime['title_jp']:
                print(f"   日文标题: {anime['title_jp']}")
            print(f"   封面: {anime['cover_image']}")
            print(f"   工作室: {anime['studio']}")
            print(f"   年份: {anime['release_year']}")
            
        # 3. 查找可疑数据模式
        print("\n" + "=" * 80)
        print("查找可疑数据:")
        print("=" * 80)
        
        # 模式1: 标题中包含多个数字（如"樱花工程师 第二季 7214 7214"）
        cursor.execute("""
            SELECT id, title, title_jp, cover_image 
            FROM animes 
            WHERE title REGEXP '[0-9]{4}' 
               OR title LIKE '% % % % %'  -- 标题中有很多空格
            LIMIT 30
        """)
        suspicious = cursor.fetchall()
        
        print(f"\n找到 {len(suspicious)} 条可能有问题的数据:")
        for i, anime in enumerate(suspicious, 1):
            print(f"{i}. ID: {anime['id']} - 标题: {anime['title']}")
        
        # 4. 统计各个工作室的动漫数量
        print("\n" + "=" * 80)
        print("工作室统计:")
        print("=" * 80)
        
        cursor.execute("""
            SELECT studio, COUNT(*) as count 
            FROM animes 
            GROUP BY studio 
            ORDER BY count DESC 
            LIMIT 20
        """)
        studios = cursor.fetchall()
        
        for s in studios:
            print(f"{s['studio']}: {s['count']}")
        
        cursor.close()
        
    except Error as e:
        print(f"数据库错误: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    analyze_data()
