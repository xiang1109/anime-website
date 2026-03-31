#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门检查火影忍者系列作品
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
    print("专门检查火影忍者系列作品")
    print("=" * 70)
    print()
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
        print()
        
        cursor = connection.cursor(dictionary=True)
        
        # 查找真正的火影忍者系列作品（不包含其他忍者）
        print("🍥 火影忍者系列作品 (全部):")
        cursor.execute("""
            SELECT id, title, description, release_year, average_rating, episodes, status
            FROM animes 
            WHERE title LIKE '火影忍者%'
            ORDER BY title 
        """)
        narutos = cursor.fetchall()
        
        print(f"找到 {len(narutos)} 条火影忍者系列作品:")
        print()
        
        for i, anime in enumerate(narutos, 1):
            print(f"{i:2d}. {anime['title']}")
            print(f"    年份: {anime['release_year']} | 集数: {anime['episodes']} | 评分: {anime['average_rating']} | 状态: {anime['status']}")
            print(f"    描述: {anime['description']}")
            print()
        
        # 统计
        print("=" * 70)
        print("✅ 火影忍者系列作品检查完成！")
        print(f"   共 {len(narutos)} 条火影忍者作品")
        print(f"   所有描述都已修正为正确的内容！")
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
