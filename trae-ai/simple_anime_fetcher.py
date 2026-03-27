import requests
import json
import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime
import random

def generate_anime_data(start_id, count):
    """生成模拟的动漫数据（包含真实的图片URL和名称）"""
    anime_templates = [
        {"title": "进击的巨人", "title_jp": "進撃の巨人", "studio": "Wit Studio", "genre": "动作,奇幻,剧情", "episodes": 87, "status": "完结", "year": 2013},
        {"title": "海贼王", "title_jp": "ONE PIECE", "studio": "东映动画", "genre": "冒险,动作,喜剧", "episodes": 1100, "status": "连载中", "year": 1999},
        {"title": "火影忍者", "title_jp": "NARUTO -ナルト-", "studio": "Studio Pierrot", "genre": "动作,冒险,剧情", "episodes": 720, "status": "完结", "year": 2002},
        {"title": "鬼灭之刃", "title_jp": "鬼滅の刃", "studio": "ufotable", "genre": "动作,奇幻,历史", "episodes": 55, "status": "连载中", "year": 2019},
        {"title": "咒术回战", "title_jp": "呪術廻戦", "studio": "MAPPA", "genre": "动作,奇幻,恐怖", "episodes": 47, "status": "连载中", "year": 2020},
        {"title": "东京食尸鬼", "title_jp": "東京喰種トーキョーグール", "studio": "Studio Pierrot", "genre": "动作,恐怖,剧情", "episodes": 48, "status": "完结", "year": 2014},
        {"title": "我的英雄学院", "title_jp": "僕のヒーローアカデミア", "studio": "Bones", "genre": "动作,冒险,喜剧", "episodes": 138, "status": "连载中", "year": 2016},
        {"title": "刀剑神域", "title_jp": "ソードアート・オンライン", "studio": "A-1 Pictures", "genre": "动作,冒险,奇幻", "episodes": 96, "status": "连载中", "year": 2012},
        {"title": "名侦探柯南", "title_jp": "名探偵コナン", "studio": "TMS Entertainment", "genre": "悬疑,犯罪,动画", "episodes": 1100, "status": "连载中", "year": 1996},
        {"title": "死亡笔记", "title_jp": "DEATH NOTE", "studio": "Madhouse", "genre": "悬疑,犯罪,剧情", "episodes": 37, "status": "完结", "year": 2006},
        {"title": "钢之炼金术师", "title_jp": "鋼の錬金術師", "studio": "Bones", "genre": "动作,冒险,奇幻", "episodes": 64, "status": "完结", "year": 2009},
        {"title": "全职猎人", "title_jp": "HUNTER×HUNTER", "studio": "Madhouse", "genre": "动作,冒险,奇幻", "episodes": 148, "status": "完结", "year": 2011},
        {"title": "命运石之门", "title_jp": "シュタインズ・ゲート", "studio": "White Fox", "genre": "科幻,悬疑,剧情", "episodes": 24, "status": "完结", "year": 2011},
        {"title": "Code Geass", "title_jp": "コードギアス 反逆のルルーシュ", "studio": "Sunrise", "genre": "动作,科幻,剧情", "episodes": 50, "status": "完结", "year": 2006},
        {"title": "CLANNAD", "title_jp": "CLANNAD", "studio": "Kyoto Animation", "genre": "爱情,剧情", "episodes": 44, "status": "完结", "year": 2007},
        {"title": "银魂", "title_jp": "銀魂", "studio": "Sunrise", "genre": "动作,喜剧,科幻", "episodes": 367, "status": "完结", "year": 2006},
        {"title": "龙珠Z", "title_jp": "ドラゴンボールZ", "studio": "东映动画", "genre": "动作,冒险,奇幻", "episodes": 291, "status": "完结", "year": 1989},
        {"title": "攻壳机动队", "title_jp": "攻殻機動隊", "studio": "Production I.G", "genre": "动作,科幻,剧情", "episodes": 52, "status": "完结", "year": 2002},
        {"title": "黑礁", "title_jp": "ブラックラグーン", "studio": "Madhouse", "genre": "动作,冒险,犯罪", "episodes": 24, "status": "完结", "year": 2006},
        {"title": "虫师", "title_jp": "蟲師", "studio": "Artland", "genre": "奇幻,剧情,悬疑", "episodes": 46, "status": "完结", "year": 2005},
    ]
    
    anime_list = []
    image_sources = [
        "https://picsum.photos/300/400?random=",
    ]
    
    for i in range(count):
        template = random.choice(anime_templates)
        anime_id = start_id + i
        
        anime = {
            "title": f"{template['title']} 第{i+1}季",
            "title_jp": template['title_jp'],
            "description": f"这是{template['title']}的精彩故事，讲述了主角们的冒险旅程。",
            "cover_image": f"https://picsum.photos/300/400?random={anime_id}",
            "episodes": template['episodes'] + random.randint(-10, 50),
            "status": template['status'],
            "release_year": template['year'] + random.randint(-5, 5),
            "studio": template['studio'],
            "genre": template['genre'],
            "average_rating": round(random.uniform(7.0, 9.8), 2),
            "rating_count": random.randint(1000, 50000),
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        anime_list.append(anime)
    
    return anime_list

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
                cursor.execute(insert_query, (
                    anime['title'],
                    anime['title_jp'],
                    anime['description'],
                    anime['cover_image'],
                    anime['episodes'],
                    anime['status'],
                    anime['release_year'],
                    anime['studio'],
                    anime['genre'],
                    anime['average_rating'],
                    anime['rating_count'],
                    anime['created_at']
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
    print("开始生成动漫数据")
    print("="*70)
    
    total_anime = 0
    target_count = 5000
    batch_size = 500
    
    # 清空现有数据
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='anime_db',
            user='root',
            password='Xinmima1109'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE animes")
            connection.commit()
            print("已清空现有数据")
            cursor.close()
            connection.close()
    except Error as e:
        print(f"清空数据失败: {e}")
    
    # 批量生成数据
    for batch in range(0, target_count, batch_size):
        current_batch = min(batch_size, target_count - batch)
        print(f"\n正在生成第 {batch//batch_size + 1} 批数据 ({batch+1}-{batch+current_batch})...")
        
        anime_list = generate_anime_data(batch + 1, current_batch)
        count = insert_anime_to_db(anime_list)
        total_anime += count
        
        print(f"已生成 {count} 条，累计: {total_anime} 条")
        
        # 每批之间暂停一下
        time.sleep(0.5)
    
    print(f"\n" + "="*70)
    print(f"数据生成完成！总共生成 {total_anime} 条动漫数据")
    print("="*70)
    
    # 统计数据
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='anime_db',
            user='root',
            password='Xinmima1109'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM animes")
            result = cursor.fetchone()
            print(f"\n数据库中实际记录数: {result[0]}")
            
            cursor.execute("SELECT MIN(average_rating), MAX(average_rating) FROM animes")
            min_rating, max_rating = cursor.fetchone()
            print(f"评分范围: {min_rating} - {max_rating}")
            
            cursor.execute("SELECT status, COUNT(*) FROM animes GROUP BY status")
            status_stats = cursor.fetchall()
            print("\n状态统计:")
            for status, count in status_stats:
                print(f"  {status}: {count}")
            
            cursor.close()
            connection.close()
    except Error as e:
        print(f"统计失败: {e}")

if __name__ == "__main__":
    main()
