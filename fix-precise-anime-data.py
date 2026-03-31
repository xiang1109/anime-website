#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确修复真实动漫数据 - 只更新完全匹配的热门作品
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

# 真实动漫数据库 - 只包含最核心的热门作品
PRECISE_ANIME_DATABASE = [
    {
        'title': '火影忍者',
        'title_jp': 'NARUTO - ナルト',
        'description': '在木叶忍者村中，鸣人从一个被孤立的孩子成长为拯救世界的英雄，讲述了友情、努力、胜利的热血故事。',
        'studio': 'Studio Pierrot',
        'genre': '热血',
        'year': 2002,
        'episodes': 720,
        'rating': 9.0
    },
    {
        'title': '火影忍者疾风传',
        'title_jp': 'NARUTO - ナルト - 疾風伝',
        'description': '鸣人长大成人，面对更强大的敌人，揭开晓组织的阴谋，为世界和平而战。',
        'studio': 'Studio Pierrot',
        'genre': '热血',
        'year': 2007,
        'episodes': 500,
        'rating': 9.2
    },
    {
        'title': '海贼王',
        'title_jp': 'ONE PIECE',
        'description': '草帽海贼团在伟大航路冒险，寻找传说中的One Piece，讲述了自由、友情、梦想的传奇故事。',
        'studio': '东映动画',
        'genre': '冒险',
        'year': 1999,
        'episodes': 1100,
        'rating': 9.5
    },
    {
        'title': '进击的巨人',
        'title_jp': '進撃の巨人',
        'description': '人类与巨人的生存之战，艾伦和同伴们为了自由而战，揭开世界的真相。',
        'studio': 'WIT STUDIO',
        'genre': '热血',
        'year': 2013,
        'episodes': 87,
        'rating': 9.7
    },
    {
        'title': '鬼灭之刃',
        'title_jp': '鬼滅の刃',
        'description': '炭治郎为了拯救变成鬼的妹妹，加入鬼杀队，与恶鬼展开殊死搏斗。',
        'studio': 'ufotable',
        'genre': '战斗',
        'year': 2019,
        'episodes': 26,
        'rating': 9.4
    },
    {
        'title': '咒术回战',
        'title_jp': '呪術廻戦',
        'description': '高中生虎杖悠仁吞下诅咒之王两面宿傩的手指，成为咒术师守护世界。',
        'studio': 'MAPPA',
        'genre': '战斗',
        'year': 2020,
        'episodes': 24,
        'rating': 9.3
    },
    {
        'title': '名侦探柯南',
        'title_jp': '名探偵コナン',
        'description': '工藤新一被神秘组织变小，化名柯南解决各种离奇案件，寻找恢复身体的方法。',
        'studio': '东映动画',
        'genre': '推理',
        'year': 1996,
        'episodes': 1100,
        'rating': 9.2
    },
    {
        'title': '银魂',
        'title_jp': '銀魂',
        'description': '在天人来袭的江户时代，万事屋坂田银时和同伴们的搞笑日常与热血冒险。',
        'studio': '日升动画',
        'genre': '喜剧',
        'year': 2006,
        'episodes': 367,
        'rating': 9.6
    },
    {
        'title': '全职猎人',
        'title_jp': 'HUNTER×HUNTER',
        'description': '小杰寻找父亲的旅程，参加猎人考试，结识伙伴，在危险世界中成长。',
        'studio': 'Madhouse',
        'genre': '冒险',
        'year': 2011,
        'episodes': 148,
        'rating': 9.5
    },
    {
        'title': '钢之炼金术师FA',
        'title_jp': '鋼の錬金術師 FULLMETAL ALCHEMIST',
        'description': '爱德华和阿尔冯斯兄弟为了复活母亲进行人体炼成，付出惨痛代价后踏上寻找贤者之石的旅程。',
        'studio': 'BONES',
        'genre': '奇幻',
        'year': 2009,
        'episodes': 64,
        'rating': 9.8
    },
    {
        'title': '灌篮高手',
        'title_jp': 'SLAM DUNK',
        'description': '不良少年樱木花道为了追求赤木晴子加入篮球队，带领湘北高中征战全国大赛。',
        'studio': '东映动画',
        'genre': '运动',
        'year': 1993,
        'episodes': 101,
        'rating': 9.7
    },
    {
        'title': '网球王子',
        'title_jp': 'テニスの王子様',
        'description': '天才少年越前龙马加入青春学园网球部，与队友们一起征战全国大赛。',
        'studio': 'NAS',
        'genre': '运动',
        'year': 2001,
        'episodes': 178,
        'rating': 8.5
    },
    {
        'title': '死神',
        'title_jp': 'BLEACH',
        'description': '黑崎一护获得死神力量，守护人类灵魂，与虚和灭却师展开激烈战斗。',
        'studio': 'Studio Pierrot',
        'genre': '战斗',
        'year': 2004,
        'episodes': 366,
        'rating': 8.8
    },
    {
        'title': '龙珠Z',
        'title_jp': 'ドラゴンボールZ',
        'description': '孙悟空变身为超级赛亚人，保护地球免受宇宙强敌的威胁。',
        'studio': '东映动画',
        'genre': '战斗',
        'year': 1989,
        'episodes': 291,
        'rating': 9.5
    },
    {
        'title': '刀剑神域',
        'title_jp': 'ソードアート・オンライン',
        'description': '桐人被困在死亡游戏中，必须通关才能离开，在游戏世界中经历冒险与爱情。',
        'studio': 'A-1 Pictures',
        'genre': '科幻',
        'year': 2012,
        'episodes': 25,
        'rating': 8.5
    },
    {
        'title': '三体',
        'title_jp': '',
        'description': '叶文洁向宇宙发出信号，引来三体文明，人类面临前所未有的危机。',
        'studio': '艺画开天',
        'genre': '科幻',
        'year': 2022,
        'episodes': 15,
        'rating': 8.8
    },
    {
        'title': '中国奇谭',
        'title_jp': '',
        'description': '八个中国风格的奇幻故事，展现传统文化的魅力。',
        'studio': '上海美术电影制片厂',
        'genre': '奇幻',
        'year': 2023,
        'episodes': 8,
        'rating': 9.5
    },
    {
        'title': '罗小黑战记',
        'title_jp': '',
        'description': '猫妖罗小黑在人类世界中冒险，与小白成为朋友。',
        'studio': '寒木春华',
        'genre': '治愈',
        'year': 2011,
        'episodes': 40,
        'rating': 9.6
    }
]

def main():
    """主函数"""
    print("=" * 70)
    print("精确修复真实动漫数据 - 只更新完全匹配的热门作品")
    print("=" * 70)
    print()
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
        print()
        
        cursor = connection.cursor(dictionary=True)
        
        update_count = 0
        
        for anime_data in PRECISE_ANIME_DATABASE:
            # 只查找完全匹配的作品
            cursor.execute("""
                SELECT id, title 
                FROM animes 
                WHERE title = %s
            """, (anime_data['title'],))
            
            match = cursor.fetchone()
            
            if match:
                # 更新数据 - 使用作品名作为seed确保封面匹配
                title_seed = anime_data['title'].replace(' ', '-')
                
                cursor.execute("""
                    UPDATE animes 
                    SET title_jp = %s,
                        description = %s,
                        studio = %s,
                        genre = %s,
                        release_year = %s,
                        episodes = %s,
                        average_rating = %s,
                        cover_image = %s,
                        nationality = %s,
                        anime_type = %s,
                        status = %s
                    WHERE id = %s
                """, (
                    anime_data['title_jp'],
                    anime_data['description'],
                    anime_data['studio'],
                    anime_data['genre'],
                    anime_data['year'],
                    anime_data['episodes'],
                    anime_data['rating'],
                    f"https://picsum.photos/seed/{title_seed}/300/400",
                    '中国' if anime_data['title_jp'] == '' else '日本',
                    anime_data['genre'],
                    '已完结',
                    match['id']
                ))
                
                update_count += 1
                print(f"✓ 精确更新: {match['title']}")
            else:
                print(f"⚠️ 未找到: {anime_data['title']} (跳过)")
        
        connection.commit()
        
        print()
        print("=" * 70)
        print(f"精确修复完成！")
        print(f"成功更新: {update_count} 条热门动漫数据")
        print("=" * 70)
        
        # 展示更新后的作品
        print()
        print("📌 精确更新后的作品:")
        cursor.execute("""
            SELECT id, title, title_jp, description, studio, genre, release_year, episodes, average_rating, cover_image
            FROM animes 
            WHERE title IN ({})
            ORDER BY FIELD(title, {})
        """.format(
            ','.join(['%s'] * len(PRECISE_ANIME_DATABASE)),
            ','.join(['%s'] * len(PRECISE_ANIME_DATABASE))
        ), [a['title'] for a in PRECISE_ANIME_DATABASE] * 2)
        
        examples = cursor.fetchall()
        
        for i, anime in enumerate(examples, 1):
            print(f"\n{i}. {anime['title']}")
            print(f"   日文: {anime['title_jp'] or '(中国动漫)'}")
            print(f"   年份: {anime['release_year']} | 集数: {anime['episodes']} | 评分: {anime['average_rating']}")
            print(f"   制作: {anime['studio']} | 类型: {anime['genre']}")
            print(f"   描述: {anime['description'][:50]}...")
            print(f"   封面: {anime['cover_image']}")
        
    except Error as e:
        print(f"数据库错误: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.rollback()
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print()
            print("数据库连接已关闭")

if __name__ == "__main__":
    main()
