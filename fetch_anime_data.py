import requests
import json
import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime

def fetch_anime_from_jikan(page=1, limit=25):
    """从Jikan API获取动漫数据"""
    try:
        url = f"https://api.jikan.moe/v4/anime?page={page}&limit={limit}&order_by=score&sort=desc"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f"API请求失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []

def fetch_anime_from_anilist(page=1, per_page=50):
    """从Anilist API获取动漫数据"""
    query = """
    query ($page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: ANIME, sort: SCORE_DESC) {
                id
                title {
                    romaji
                    english
                    native
                }
                description
                coverImage {
                    large
                    medium
                }
                episodes
                status
                startDate {
                    year
                }
                studios {
                    nodes {
                        name
                    }
                }
                genres
                averageScore
                popularity
            }
        }
    }
    """
    variables = {
        'page': page,
        'perPage': per_page
    }
    
    try:
        url = 'https://graphql.anilist.co'
        response = requests.post(url, json={'query': query, 'variables': variables}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('Page', {}).get('media', [])
        else:
            print(f"Anilist API请求失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"获取Anilist数据失败: {e}")
        return []

def clean_html(text):
    """清理HTML标签"""
    if not text:
        return ""
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('\n', ' ').replace('\r', '')
    return text[:500] if len(text) > 500 else text

def insert_anime_to_db(anime_list):
    """将动漫数据插入数据库"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='anime_db',
            user='root',
            password='Xinmima1109'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            insert_query = """
            INSERT IGNORE INTO animes 
            (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            inserted_count = 0
            for anime in anime_list:
                # 提取数据
                title = anime.get('title', '')
                if isinstance(title, dict):
                    title = title.get('english', '') or title.get('romaji', '') or title.get('native', '')
                
                title_jp = ''
                if isinstance(anime.get('title'), dict):
                    title_jp = anime.get('title', {}).get('native', '') or anime.get('title', {}).get('romaji', '')
                
                description = clean_html(anime.get('description', ''))
                
                cover_image = ''
                if anime.get('cover_image'):
                    cover_image = anime.get('cover_image', '')
                elif anime.get('coverImage'):
                    cover_image = anime.get('coverImage', {}).get('large', '') or anime.get('coverImage', {}).get('medium', '')
                
                episodes = anime.get('episodes') or 0
                status_map = {'FINISHED': '完结', 'RELEASING': '连载中', 'NOT_YET_RELEASED': '未播出'}
                status = status_map.get(anime.get('status', ''), anime.get('status', ''))
                release_year = anime.get('release_year') or anime.get('startDate', {}).get('year') or 0
                
                studio = ''
                if anime.get('studios'):
                    if isinstance(anime.get('studios'), list):
                        studio = anime.get('studios', [{}])[0].get('name', '')
                    elif isinstance(anime.get('studios'), dict):
                        studio = anime.get('studios', {}).get('name', '')
                
                genre = ', '.join(anime.get('genres', [])) if anime.get('genres') else ''
                average_rating = float(anime.get('average_rating') or anime.get('averageScore') or 0) / 10
                rating_count = anime.get('rating_count') or anime.get('popularity') or 0
                
                created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # 插入数据
                cursor.execute(insert_query, (
                    title, title_jp, description, cover_image, episodes, status,
                    release_year, studio, genre, average_rating, rating_count, created_at
                ))
                inserted_count += 1
            
            connection.commit()
            print(f"成功插入 {inserted_count} 条动漫数据")
            return inserted_count
            
    except Error as e:
        print(f"数据库错误: {e}")
        return 0
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    print("="*70)
    print("开始获取动漫数据")
    print("="*70)
    
    total_anime = 0
    target_count = 5000
    
    # 使用多种API源获取数据
    sources = [
        {'name': 'Jikan', 'fetch_func': fetch_anime_from_jikan, 'pages': 40},
        {'name': 'Anilist', 'fetch_func': fetch_anime_from_anilist, 'pages': 100},
    ]
    
    for source in sources:
        if total_anime >= target_count:
            break
            
        print(f"\n从 {source['name']} 获取数据...")
        
        for page in range(1, source['pages'] + 1):
            if total_anime >= target_count:
                break
                
            print(f"  正在获取第 {page} 页...")
            anime_list = source['fetch_func'](page)
            
            if anime_list:
                count = insert_anime_to_db(anime_list)
                total_anime += count
                print(f"  已获取 {count} 条，累计: {total_anime} 条")
            else:
                print(f"  第 {page} 页没有数据")
            
            # 避免API限流
            time.sleep(1)
    
    print(f"\n" + "="*70)
    print(f"数据获取完成！总共获取 {total_anime} 条动漫数据")
    print("="*70)

if __name__ == "__main__":
    main()
