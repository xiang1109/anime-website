#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证和统计动漫数据库
"""

import mysql.connector
from mysql.connector import Error

# 数据库配置
DB_CONFIG = {
    'host': '59.110.214.50',
    'port': 3306,
    'user': 'anime_user',
    'password': 'Xinmima1109',
    'database': 'anime_db',
    'charset': 'utf8mb4'
}

def main():
    """主函数"""
    print("=" * 70)
    print("动漫数据库统计验证")
    print("=" * 70)
    print()
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
        print()
        
        cursor = connection.cursor(dictionary=True)
        
        # 1. 总数量
        cursor.execute("SELECT COUNT(*) as total FROM animes")
        result = cursor.fetchone()
        total = result['total']
        print(f"📊 动漫总数量: {total:,} 条")
        print()
        
        # 2. 按国籍统计
        print("🌍 按国籍统计:")
        cursor.execute("""
            SELECT nationality, COUNT(*) as count 
            FROM animes 
            GROUP BY nationality 
            ORDER BY count DESC
        """)
        nationalities = cursor.fetchall()
        for nat in nationalities:
            print(f"  {nat['nationality']}: {nat['count']:,} 条")
        print()
        
        # 3. 按状态统计
        print("📋 按状态统计:")
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM animes 
            GROUP BY status 
            ORDER BY count DESC
        """)
        statuses = cursor.fetchall()
        for stat in statuses:
            print(f"  {stat['status']}: {stat['count']:,} 条")
        print()
        
        # 4. 按类型统计
        print("🎭 按类型统计 (Top 15):")
        cursor.execute("""
            SELECT anime_type, COUNT(*) as count 
            FROM animes 
            WHERE anime_type IS NOT NULL AND anime_type != ''
            GROUP BY anime_type 
            ORDER BY count DESC
            LIMIT 15
        """)
        types = cursor.fetchall()
        for typ in types:
            print(f"  {typ['anime_type']}: {typ['count']:,} 条")
        print()
        
        # 5. 按年份统计
        print("📅 按年份统计 (Top 10):")
        cursor.execute("""
            SELECT release_year, COUNT(*) as count 
            FROM animes 
            WHERE release_year IS NOT NULL
            GROUP BY release_year 
            ORDER BY count DESC
            LIMIT 10
        """)
        years = cursor.fetchall()
        for yr in years:
            print(f"  {yr['release_year']}年: {yr['count']:,} 条")
        print()
        
        # 6. 评分统计
        print("⭐ 评分统计:")
        cursor.execute("SELECT MIN(average_rating) as min_rating FROM animes WHERE average_rating IS NOT NULL")
        min_rating = cursor.fetchone()['min_rating']
        cursor.execute("SELECT MAX(average_rating) as max_rating FROM animes WHERE average_rating IS NOT NULL")
        max_rating = cursor.fetchone()['max_rating']
        cursor.execute("SELECT AVG(average_rating) as avg_rating FROM animes WHERE average_rating IS NOT NULL")
        avg_rating = cursor.fetchone()['avg_rating']
        
        print(f"  最低评分: {min_rating}")
        print(f"  最高评分: {max_rating}")
        print(f"  平均评分: {avg_rating:.2f}")
        print()
        
        # 7. 高分作品 (9.0+)
        cursor.execute("SELECT COUNT(*) as high_rated FROM animes WHERE average_rating >= 9.0")
        high_rated = cursor.fetchone()['high_rated']
        print(f"🏆 高分作品(9.0+): {high_rated:,} 条")
        
        # 8. 剧场版
        cursor.execute("SELECT COUNT(*) as movies FROM animes WHERE is_movie = 1")
        movies = cursor.fetchone()['movies']
        print(f"🎬 剧场版/电影: {movies:,} 条")
        print()
        
        # 9. 展示一些最近添加的数据
        print("📌 最近添加的20条作品:")
        cursor.execute("""
            SELECT title, release_year, average_rating, rating_count, nationality, status
            FROM animes 
            ORDER BY id DESC 
            LIMIT 20
        """)
        recent = cursor.fetchall()
        for i, anime in enumerate(recent, 1):
            print(f"  {i:2d}. {anime['title']} ({anime['release_year']}) - {anime['average_rating']}分 - {anime['nationality']} - {anime['status']}")
        print()
        
        # 10. 展示一些高分作品
        print("🏆 Top 20 高分作品:")
        cursor.execute("""
            SELECT title, release_year, average_rating, rating_count, nationality
            FROM animes 
            ORDER BY average_rating DESC, rating_count DESC
            LIMIT 20
        """)
        top = cursor.fetchall()
        for i, anime in enumerate(top, 1):
            print(f"  {i:2d}. {anime['title']} ({anime['release_year']}) - {anime['average_rating']}分 - {anime['rating_count']:,}人评价 - {anime['nationality']}")
        print()
        
        print("=" * 70)
        print("✓ 数据库验证完成！")
        print(f"  总数据量: {total:,} 条动漫作品")
        print("=" * 70)
        
    except Error as e:
        print(f"数据库错误: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print()
            print("数据库连接已关闭")

if __name__ == "__main__":
    main()
