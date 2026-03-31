import mysql.connector
from mysql.connector import Error
import random

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

def analyze_images():
    connection = create_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        print("=" * 60)
        print("分析动漫图片数据")
        print("=" * 60)
        
        # 1. 获取总数据量
        cursor.execute("SELECT COUNT(*) as total FROM animes")
        total_count = cursor.fetchone()['total']
        print(f"\n总动漫数量: {total_count}")
        
        # 2. 随机查看一些动漫数据
        print("\n" + "=" * 60)
        print("随机抽取20条动漫数据样本:")
        print("=" * 60)
        
        cursor.execute("""
            SELECT id, title, title_jp, cover_image, studio, release_year, description 
            FROM animes 
            ORDER BY RAND() 
            LIMIT 20
        """)
        animes = cursor.fetchall()
        
        for i, anime in enumerate(animes, 1):
            print(f"\n{i}. ID: {anime['id']}")
            print(f"   标题: {anime['title']}")
            if anime['title_jp']:
                print(f"   日文标题: {anime['title_jp']}")
            print(f"   封面图片: {anime['cover_image']}")
            print(f"   工作室: {anime['studio']}")
            print(f"   年份: {anime['release_year']}")
            if anime['description']:
                print(f"   描述: {anime['description'][:100]}...")
        
        # 3. 检查图片URL格式
        print("\n" + "=" * 60)
        print("图片URL分析:")
        print("=" * 60)
        
        cursor.execute("SELECT cover_image FROM animes LIMIT 100")
        all_images = cursor.fetchall()
        
        picsum_count = 0
        other_count = 0
        
        for img in all_images:
            url = img['cover_image'] or ''
            if 'picsum.photos' in url:
                picsum_count += 1
            else:
                other_count += 1
        
        print(f"\n使用picsum.photos的图片: {picsum_count}")
        print(f"其他图片: {other_count}")
        
        # 4. 建议方案说明
        print("\n" + "=" * 60)
        print("图片优化方案:")
        print("=" * 60)
        print("""
当前问题：
1. 大部分图片使用picsum.photos的随机图片，与动漫内容不符

优化方案：
方案1: 使用动漫数据库API（如Bangumi、MyAnimeList等）
方案2: 手动整理真实动漫图片库
方案3: 使用搜索引擎图片搜索API
方案4: 创建动漫图片托管服务

注意事项：
- 需要遵守版权法律
- 需要API调用限制
- 需要图片缓存机制
- 需要错误处理和重试机制
        """)
        
        cursor.close()
        
    except Error as e:
        print(f"数据库错误: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    analyze_images()
