import requests
import json
import mysql.connector
from datetime import datetime

def fetch_anime_data(page=1, per_page=50):
    url = f'https://api.jikan.moe/v4/top/anime?page={page}&limit={per_page}'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'API请求失败: {response.status_code}')
            return None
    except Exception as e:
        print(f'请求异常: {e}')
        return None

def clean_anime_data(anime):
    title = anime.get('title', '')
    title_jp = anime.get('title_japanese', '') or ''
    
    if title_jp == '':
        title_jp = anime.get('title', '')
    
    description = anime.get('synopsis', '') or ''
    if description == '':
        description = f'这是一部关于{title}的精彩动漫'
    
    cover_image = anime.get('images', {}).get('jpg', {}).get('large_image_url', '') or ''
    if cover_image == '':
        cover_image = anime.get('images', {}).get('jpg', {}).get('image_url', '') or ''
    
    episodes = anime.get('episodes', 0)
    if episodes is None or episodes == 0:
        episodes = 12
    
    status = anime.get('status', '') or ''
    if status == '':
        status = '未知'
    
    release_year = anime.get('year', 0)
    if release_year is None or release_year == 0:
        release_year = 2023
    
    studio = ''
    studios = anime.get('studios', [])
    if studios and len(studios) > 0:
        studio = studios[0].get('name', '')
    if studio == '':
        studio = '未知工作室'
    
    genre_list = []
    genres = anime.get('genres', [])
    for genre in genres:
        genre_name = genre.get('name', '')
        if genre_name:
            genre_list.append(genre_name)
    if len(genre_list) == 0:
        genre_list = ['动作', '冒险']
    genre = ','.join(genre_list)
    
    average_rating = anime.get('score', 0)
    if average_rating is None or average_rating == 0:
        average_rating = 7.5
    average_rating = round(average_rating, 2)
    
    rating_count = anime.get('members', 0)
    if rating_count is None or rating_count == 0:
        rating_count = 1000
    
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at)

def main():
    conn = mysql.connector.connect(
        host='59.110.214.50',
        database='anime_db',
        user='root',
        password='Xinmima1109'
    )
    cursor = conn.cursor()
    
    print('清空现有数据...')
    cursor.execute('TRUNCATE TABLE animes')
    conn.commit()
    print('已清空')
    
    insert_query = 'INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    
    total_pages = 20
    all_anime_data = []
    
    print(f'开始获取动漫数据...')
    
    for page in range(1, total_pages + 1):
        print(f'正在获取第 {page} 页...')
        data = fetch_anime_data(page=page, per_page=50)
        
        if data and 'data' in data:
            anime_list = data['data']
            print(f'  获取到 {len(anime_list)} 条数据')
            
            for anime in anime_list:
                cleaned_data = clean_anime_data(anime)
                all_anime_data.append(cleaned_data)
            
            print(f'  累计: {len(all_anime_data)} 条')
        else:
            print(f'  获取失败')
    
    print(f'\n总共获取到 {len(all_anime_data)} 条数据')
    
    if len(all_anime_data) > 0:
        print('开始插入数据库...')
        cursor.executemany(insert_query, all_anime_data)
        conn.commit()
        print(f'成功插入 {cursor.rowcount} 条记录')
        
        cursor.execute('SELECT COUNT(*) FROM animes')
        print(f'总记录数: {cursor.fetchone()[0]}')
        
        cursor.execute('SELECT id, title, average_rating FROM animes ORDER BY id DESC LIMIT 5')
        print('\n最后5条数据:')
        for row in cursor.fetchall():
            print(row)
    else:
        print('没有获取到数据')
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
