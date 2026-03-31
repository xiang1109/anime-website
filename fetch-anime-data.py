#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动漫数据获取和更新脚本
用于从第三方API获取动漫数据并更新到数据库
"""

import mysql.connector
from mysql.connector import Error
import requests
import json
from datetime import datetime, timedelta
import random
import time

# 数据库配置
DB_CONFIG = {
    'host': '59.110.214.50',
    'port': 3306,
    'user': 'anime_user',
    'password': 'Xinmima1109',
    'database': 'anime_db',
    'charset': 'utf8mb4'
}

# 示例动漫数据（模拟API返回的数据结构
SAMPLE_ANIME_DATA = [
    {
        'title': '葬送的芙莉莲',
        'title_jp': '葬送のフリーレン',
        'description': '讲述了精灵魔法使芙莉莲与勇者一行人完成了打倒魔王的任务后，与勇者们各自回归了各自的生活，而芙莉莲则开始了新的旅程。',
        'cover_image': 'https://picsum.photos/seed/frieren/300/400',
        'episodes': 28,
        'status': '已完结',
        'release_year': 2024,
        'release_date': '2024-01-05',
        'studio': 'Madhouse',
        'genre': '奇幻,冒险',
        'average_rating': 9.2,
        'rating_count': 120000,
        'nationality': '日本',
        'anime_type': '奇幻',
        'is_movie': 0
    },
    {
        'title': '迷宫饭 第二季',
        'title_jp': 'ダンジョン飯 第2期',
        'description': '继续讲述莱欧斯一行在迷宫中寻找被龙并吃掉各种魔物的冒险故事。',
        'cover_image': 'https://picsum.photos/seed/dungeon2/300/400',
        'episodes': 24,
        'status': '已完结',
        'release_year': 2025,
        'release_date': '2025-01-10',
        'studio': 'TRIGGER',
        'genre': '奇幻,喜剧',
        'average_rating': 8.9,
        'rating_count': 95000,
        'nationality': '日本',
        'anime_type': '奇幻',
        'is_movie': 0
    },
    {
        'title': '药屋少女的呢喃 第二季',
        'title_jp': '薬屋のひとりごと 第2期',
        'description': '猫猫继续在后宫中用她的医学知识解决各种问题。',
        'cover_image': 'https://picsum.photos/seed/kusuriya2/300/400',
        'episodes': 26,
        'status': '已完结',
        'release_year': 2025,
        'release_date': '2025-01-15',
        'studio': 'TOHO animation',
        'genre': '历史,悬疑',
        'average_rating': 9.0,
        'rating_count': 110000,
        'nationality': '日本',
        'anime_type': '悬疑',
        'is_movie': 0
    },
    {
        'title': '怪兽8号 第二季',
        'title_jp': '怪獣8号 第2期',
        'description': '日比野卡夫卡继续作为怪兽8号守护人类。',
        'cover_image': 'https://picsum.photos/seed/kaiju2/300/400',
        'episodes': 24,
        'status': '已完结',
        'release_year': 2025,
        'release_date': '2025-01-20',
        'studio': 'Production I.G',
        'genre': '动作,科幻',
        'average_rating': 8.7,
        'rating_count': 85000,
        'nationality': '日本',
        'anime_type': '热血',
        'is_movie': 0
    },
    {
        'title': '我推的孩子 第二季',
        'title_jp': '推しの子 第2期',
        'description': '阿库亚和露比继续在娱乐圈中寻找真相。',
        'cover_image': 'https://picsum.photos/seed/oshinoko2/300/400',
        'episodes': 28,
        'status': '已完结',
        'release_year': 2025,
        'release_date': '2025-02-01',
        'studio': '动画工房',
        'genre': '剧情,悬疑',
        'average_rating': 8.8,
        'rating_count': 98000,
        'nationality': '日本',
        'anime_type': '剧情',
        'is_movie': 0
    }
]

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

def check_anime_exists(connection, title):
    """检查动漫是否已存在"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT id FROM animes WHERE title = %s', (title,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    except Error as e:
        print(f"检查动漫存在性错误: {e}")
        return False

def insert_or_update_anime(connection, anime_data):
    """插入或更新动漫数据"""
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 检查是否存在
        if check_anime_exists(connection, anime_data['title']):
            # 更新现有数据
            update_query = """
            UPDATE animes 
            SET title_jp = %s, description = %s, cover_image = %s, 
                episodes = %s, status = %s, release_year = %s,
                release_date = %s, studio = %s, genre = %s,
                average_rating = %s, rating_count = %s, nationality = %s,
                anime_type = %s, is_movie = %s
            WHERE title = %s
            """
            cursor.execute(update_query, (
                anime_data['title_jp'],
                anime_data['description'],
                anime_data['cover_image'],
                anime_data['episodes'],
                anime_data['status'],
                anime_data['release_year'],
                anime_data['release_date'],
                anime_data['studio'],
                anime_data['genre'],
                anime_data['average_rating'],
                anime_data['rating_count'],
                anime_data['nationality'],
                anime_data['anime_type'],
                anime_data['is_movie'],
                anime_data['title']
            ))
            print(f"更新动漫: {anime_data['title']}")
        else:
            # 插入新数据
            insert_query = """
            INSERT INTO animes 
            (title, title_jp, description, cover_image, episodes,
            status, release_year, release_date, studio, genre,
            average_rating, rating_count, nationality, anime_type, is_movie, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(insert_query, (
                anime_data['title'],
                anime_data['title_jp'],
                anime_data['description'],
                anime_data['cover_image'],
                anime_data['episodes'],
                anime_data['status'],
                anime_data['release_year'],
                anime_data['release_date'],
                anime_data['studio'],
                anime_data['genre'],
                anime_data['average_rating'],
                anime_data['rating_count'],
                anime_data['nationality'],
                anime_data['anime_type'],
                anime_data['is_movie']
            ))
            print(f"添加新动漫: {anime_data['title']}")
        
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        print(f"插入/更新动漫错误: {e}")
        connection.rollback()
        return False

def fetch_anime_from_api():
    """
    从第三方API获取动漫数据
    这里使用模拟数据，实际使用时可以替换为真实的API调用
    """
    print("正在获取动漫数据...")
    
    # 实际项目中可以使用以下API之一：
    # - MyAnimeList API
    # - AniList API
    # - Jikan API (MyAnimeList 非官方 API)
    
    # 这里使用示例数据
    return SAMPLE_ANIME_DATA

def main():
    """主函数"""
    print("=" * 60)
    print("动漫数据获取和更新脚本")
    print("=" * 60)
    print()
    
    # 获取数据库连接
    connection = get_db_connection()
    if not connection:
        print("无法连接到数据库，退出程序")
        return
    
    try:
        # 获取动漫数据
        anime_list = fetch_anime_from_api()
        
        print(f"获取到 {len(anime_list)} 条动漫数据")
        print()
        
        # 更新数据库
        success_count = 0
        for anime in anime_list:
            if insert_or_update_anime(connection, anime):
                success_count += 1
            time.sleep(0.5)  # 避免请求过快
        
        print()
        print("=" * 60)
        print(f"更新完成！成功处理 {success_count}/{len(anime_list)} 条数据")
        print("=" * 60)
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    main()
