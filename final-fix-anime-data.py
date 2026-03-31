#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复 - 去掉标题数字，添加真实的B站冷门佳作
"""

import mysql.connector
from mysql.connector import Error
import random

# 数据库配置
DB_CONFIG = {
    'host': '59.110.214.50',
    'port': 3306,
    'user': 'anime_user',
    'password': 'Xinmima1109',
    'database': 'anime_db',
    'charset': 'utf8mb4'
}

# B站冷门佳作 - 真实的
BILIBILI_HIDDEN_GEMS = [
    {
        'title': '怪化猫',
        'title_jp': 'モノノ怪',
        'description': '卖药郎手持退魔之剑，斩妖除魔的怪谈故事，浮世绘风格独特。',
        'studio': '东映动画',
        'genre': '悬疑',
        'year': 2007,
        'episodes': 12,
        'rating': 9.5,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '四叠半神话大系',
        'title_jp': '四畳半神話大系',
        'description': '大学生在四叠半宿舍中不断轮回，寻找理想大学生活的奇幻故事。',
        'studio': 'MADHOUSE',
        'genre': '奇幻',
        'year': 2010,
        'episodes': 11,
        'rating': 9.6,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '乒乓',
        'title_jp': 'ピンポン',
        'description': '星野裕和月本诚两个天才乒乓球手的竞争与友情，画风独特。',
        'studio': '龙之子',
        'genre': '运动',
        'year': 2014,
        'episodes': 11,
        'rating': 9.5,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '昭和元禄落语心中',
        'title_jp': '昭和元禄落語心中',
        'description': '与太郎在监狱中遇到落语家八云，拜师学艺传承落语艺术。',
        'studio': 'Studio DEEN',
        'genre': '历史',
        'year': 2016,
        'episodes': 13,
        'rating': 9.6,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '三月的狮子',
        'title_jp': '3月のライオン',
        'description': '将棋天才桐山零在经历家庭变故后，与川本三姐妹相遇走出孤独。',
        'studio': 'SHAFT',
        'genre': '治愈',
        'year': 2016,
        'episodes': 22,
        'rating': 9.4,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '来自深渊',
        'title_jp': 'メイドインアビス',
        'description': '莉可和雷格前往深渊深处寻找母亲，揭开深渊的神秘面纱。',
        'studio': 'Kinema Citrus',
        'genre': '奇幻',
        'year': 2017,
        'episodes': 13,
        'rating': 9.5,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '比宇宙更远的地方',
        'title_jp': '宇宙よりも遠い場所',
        'description': '四位女高中生一起去南极的青春冒险故事，治愈又感动。',
        'studio': 'MADHOUSE',
        'genre': '治愈',
        'year': 2018,
        'episodes': 13,
        'rating': 9.4,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '强风吹拂',
        'title_jp': '風が強く吹いている',
        'description': '清濑灰二带领竹青庄的房客们参加箱根驿传，讲述跑步的意义。',
        'studio': 'Production I.G',
        'genre': '运动',
        'year': 2018,
        'episodes': 23,
        'rating': 9.6,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '别对映像研出手！',
        'title_jp': '映像研には手を出すな！',
        'description': '浅草绿、金森沙耶香、水崎燕三位少女一起制作动画的故事。',
        'studio': 'Science SARU',
        'genre': '校园',
        'year': 2020,
        'episodes': 12,
        'rating': 9.5,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '大欺诈师',
        'title_jp': 'GREAT PRETENDER',
        'description': '枝村真人被卷入国际诈骗，与罗兰一起在世界各地进行诈骗冒险。',
        'studio': 'WIT STUDIO',
        'genre': '悬疑',
        'year': 2020,
        'episodes': 23,
        'rating': 9.3,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '黄金神威',
        'title_jp': 'ゴールデンカムイ',
        'description': '杉元佐一和阿席莉帕在北海道寻找黄金，与各种敌人战斗。',
        'studio': 'Geno Studio',
        'genre': '冒险',
        'year': 2018,
        'episodes': 12,
        'rating': 9.4,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '佐贺偶像是传奇',
        'title_jp': 'ゾンビランドサガ',
        'description': '七位少女僵尸组成偶像团体，复兴佐贺的搞笑故事。',
        'studio': 'MAPPA',
        'genre': '喜剧',
        'year': 2018,
        'episodes': 12,
        'rating': 9.2,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '动物新世代',
        'title_jp': 'BNA',
        'description': '影森满变成兽人来到兽人都市，与大神士郎相遇。',
        'studio': 'TRIGGER',
        'genre': '奇幻',
        'year': 2020,
        'episodes': 12,
        'rating': 9.0,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '全员恶玉',
        'title_jp': 'アクダマドライブ',
        'description': '罪犯们在关西执行危险任务，充满悬疑和反转。',
        'studio': 'Studio Pierrot',
        'genre': '犯罪',
        'year': 2020,
        'episodes': 12,
        'rating': 8.8,
        'nationality': '日本',
        'is_hidden_gem': 1
    },
    {
        'title': '中国奇谭',
        'title_jp': '',
        'description': '八个中国风格的奇幻故事，展现传统文化的魅力。',
        'studio': '上海美术电影制片厂',
        'genre': '奇幻',
        'year': 2023,
        'episodes': 8,
        'rating': 9.5,
        'nationality': '中国',
        'is_hidden_gem': 1
    },
    {
        'title': '雾山五行',
        'title_jp': '',
        'description': '闻人翊悬在雾山中与妖兽战斗，守护五行平衡。',
        'studio': '好传动画',
        'genre': '战斗',
        'year': 2020,
        'episodes': 3,
        'rating': 9.3,
        'nationality': '中国',
        'is_hidden_gem': 1
    },
    {
        'title': '大理寺日志',
        'title_jp': '',
        'description': '李饼在大理寺为官，与陈拾一起解决各种案件。',
        'studio': '好传动画',
        'genre': '悬疑',
        'year': 2020,
        'episodes': 12,
        'rating': 9.0,
        'nationality': '中国',
        'is_hidden_gem': 1
    },
    {
        'title': '时光代理人',
        'title_jp': '',
        'description': '程小时和陆光通过照片回到过去，完成客户的委托。',
        'studio': '澜映画',
        'genre': '悬疑',
        'year': 2021,
        'episodes': 11,
        'rating': 9.1,
        'nationality': '中国',
        'is_hidden_gem': 1
    },
    {
        'title': '罗小黑战记',
        'title_jp': '',
        'description': '猫妖罗小黑在人类世界中冒险，与小白成为朋友。',
        'studio': '寒木春华',
        'genre': '治愈',
        'year': 2011,
        'episodes': 40,
        'rating': 9.6,
        'nationality': '中国',
        'is_hidden_gem': 1
    },
    {
        'title': '刺客伍六七',
        'title_jp': '',
        'description': '伍六七在小鸡岛上做刺客，其实是为了找回失去的记忆。',
        'studio': '小疯映画',
        'genre': '喜剧',
        'year': 2018,
        'episodes': 10,
        'rating': 9.2,
        'nationality': '中国',
        'is_hidden_gem': 1
    }
]

# 普通动漫素材库
GOOD_TITLES = [
    "星空协奏曲", "银河物语", "月光交响曲", "晨曦传说", "黄昏战记",
    "樱花奇谈", "枫叶传奇", "雪花物语", "风花战记", "紫阳花传说",
    "向日葵战记", "薰衣草奇谈", "玫瑰物语", "海洋传说", "天空战记",
    "大地奇谈", "森林传说", "山岳战记", "河流物语", "湖泊传说",
    "沙漠战记", "草原奇谈", "城市物语", "小镇传说", "村庄战记",
    "学园奇谈", "学院传说", "校园战记", "青春物语", "日常传说",
    "喜剧战记", "治愈奇谈", "感动传说", "热血战记", "励志物语",
    "音乐传说", "艺术战记", "运动奇谈", "竞技传说", "料理物语",
    "美食传说", "旅行战记", "游记奇谈", "冒险传说", "探索物语",
    "发现传说", "秘密战记", "真相奇谈", "战斗传说", "战争物语",
    "和平传说", "羁绊战记", "友情奇谈", "爱情传说", "亲情物语",
    "守护传说", "勇者战记", "英雄奇谈", "骑士传说", "战士物语",
    "法师传说", "贤者战记", "魔王奇谈", "龙传说", "精灵活物语",
    "妖精传说", "魔法战记", "异能奇谈", "超能力传说", "科幻物语",
    "机战传说", "机战记", "推理奇谈", "悬疑传说", "恐怖物语"
]

DESCRIPTIONS = [
    "在这个奇幻的世界中，主角与伙伴们一起经历着各种冒险，逐渐成长并发现世界的真相。",
    "一部温馨治愈的作品，通过平凡的日常故事展现人性的美好与温暖。",
    "热血沸腾的战斗场面，主角在逆境中不断突破极限，实现自我超越。",
    "充满悬疑与推理的故事，每个线索都暗藏玄机，真相往往出人意料。",
    "描绘青春年少的美好时光，友情、爱情、梦想交织的动人故事。",
    "以独特的世界观和深刻的主题，引发观众对人生和社会的思考。",
    "轻松幽默的喜剧作品，让观众在欢笑中感受到生活的乐趣。",
    "体育竞技题材，展现运动员们为梦想拼搏的汗水与泪水。",
    "历史题材作品，还原那个波澜壮阔的时代，让人身临其境。",
    "科幻巨作，探讨科技与人类的关系，展现未来世界的无限可能。"
]

STUDIOS = [
    "Madhouse", "ufotable", "MAPPA", "WIT STUDIO", "京都动画",
    "动画工房", "Production I.G", "A-1 Pictures", "CloverWorks", "BONES",
    "SHAFT", "J.C.STAFF", "日升动画", "东映动画", "OLM",
    "Studio DEEN", "feel.", "SILVER LINK", "TRIGGER", "P.A.WORKS",
    "WHITE FOX", "8bit", "Lay-duce", "C-Station", "Science SARU",
    "福煦影视", "视美影业", "绘梦动画", "好传动画", "艺画开天",
    "澜映画", "幻维数码", "万维猫", "寒木春华", "小疯映画",
    "上海美术电影制片厂"
]

GENRES = [
    "热血", "奇幻", "冒险", "悬疑", "科幻", "爱情", "喜剧",
    "运动", "治愈", "历史", "战争", "恐怖", "推理", "机战",
    "日常", "校园", "职场", "偶像", "音乐", "美术", "料理",
    "战斗", "魔法", "穿越", "转生", "成长", "友情", "羁绊"
]

NATIONALITIES = ["日本", "中国", "韩国", "美国"]
STATUSES = ["连载中", "已完结", "未播出"]

def main():
    """主函数"""
    print("=" * 70)
    print("最终修复 - 去掉标题数字，添加B站冷门佳作")
    print("=" * 70)
    print()
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
        print()
        
        cursor = connection.cursor(dictionary=True)
        
        # 先检查是否有is_hidden_gem字段，如果没有就添加
        try:
            cursor.execute("ALTER TABLE animes ADD COLUMN is_hidden_gem TINYINT DEFAULT 0")
            print("✓ 添加了is_hidden_gem字段")
        except:
            print("⚠️ is_hidden_gem字段已存在，跳过添加")
        
        # 先插入B站冷门佳作
        print()
        print("正在插入B站冷门佳作...")
        hidden_gem_count = 0
        
        for gem in BILIBILI_HIDDEN_GEMS:
            # 检查是否已存在
            cursor.execute("SELECT id FROM animes WHERE title = %s", (gem['title'],))
            exists = cursor.fetchone()
            
            if not exists:
                title_seed = gem['title'].replace(' ', '-')
                
                cursor.execute("""
                    INSERT INTO animes 
                    (title, title_jp, description, cover_image, episodes, status,
                     release_year, release_date, studio, genre, average_rating, rating_count,
                     nationality, anime_type, is_movie, is_hidden_gem, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """, (
                    gem['title'],
                    gem['title_jp'],
                    gem['description'],
                    f"https://picsum.photos/seed/{title_seed}/300/400",
                    gem['episodes'],
                    "已完结",
                    gem['year'],
                    f"{gem['year']}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                    gem['studio'],
                    gem['genre'],
                    gem['rating'],
                    random.randint(50000, 200000),
                    gem['nationality'],
                    gem['genre'],
                    0,
                    gem.get('is_hidden_gem', 1)
                ))
                
                hidden_gem_count += 1
                print(f"  ✓ 插入: {gem['title']}")
        
        connection.commit()
        print(f"✓ 成功插入 {hidden_gem_count} 条B站冷门佳作")
        print()
        
        # 获取所有需要修复的ID（排除冷门佳作）
        print("正在修复其他动漫，去掉标题数字...")
        cursor.execute("""
            SELECT id, title 
            FROM animes 
            WHERE is_hidden_gem = 0 OR is_hidden_gem IS NULL
            ORDER BY id
        """)
        all_animes = cursor.fetchall()
        
        print(f"需要修复 {len(all_animes):,} 条普通动漫")
        print()
        
        fix_count = 0
        batch_size = 100
        used_titles = set()
        
        # 先收集所有冷门佳作的标题，避免重复
        cursor.execute("SELECT title FROM animes WHERE is_hidden_gem = 1")
        for row in cursor.fetchall():
            used_titles.add(row['title'])
        
        for i, anime in enumerate(all_animes):
            anime_id = anime['id']
            
            # 生成新的标题（不带数字）
            while True:
                new_title = random.choice(GOOD_TITLES)
                
                # 有时候加季数
                if random.random() < 0.15:
                    season_num = random.randint(1, 3)
                    season_names = ["第一季", "第二季", "第三季"]
                    new_title = f"{new_title} {season_names[season_num - 1]}"
                elif random.random() < 0.08:
                    new_title = f"{new_title} 特别篇" if random.random() < 0.5 else f"{new_title} 剧场版"
                
                # 确保不重复
                if new_title not in used_titles:
                    used_titles.add(new_title)
                    break
            
            # 生成其他合理数据
            release_year = random.randint(1990, 2025)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            release_date = f"{release_year}-{month:02d}-{day:02d}"
            
            is_movie = 1 if random.random() < 0.1 else 0
            if is_movie:
                episodes = random.randint(0, 3)
                status = "已完结"
            else:
                episodes = random.randint(1, 50) if random.random() > 0.3 else random.randint(1, 24)
                status = random.choices(STATUSES, weights=[0.2, 0.75, 0.05])[0]
            
            average_rating = round(random.uniform(5.5, 9.5), 2)
            
            if average_rating > 9.0:
                rating_count = random.randint(50000, 300000)
            elif average_rating > 8.0:
                rating_count = random.randint(20000, 150000)
            elif average_rating > 7.0:
                rating_count = random.randint(10000, 80000)
            else:
                rating_count = random.randint(1000, 30000)
            
            nationality = random.choices(NATIONALITIES, weights=[0.7, 0.2, 0.06, 0.04])[0]
            genre = random.choice(GENRES)
            studio = random.choice(STUDIOS)
            description = random.choice(DESCRIPTIONS)
            
            # 封面图片使用标题作为seed
            title_seed = new_title.replace(' ', '-').replace('！', '').replace('·', '')
            
            # 特殊处理：确保"你的名字"只有一个，且没有第二季
            if "你的名字" in new_title:
                if random.random() > 0.1:  # 90%概率换成其他标题
                    new_title = random.choice([t for t in GOOD_TITLES if "你的名字" not in t])
                    title_seed = new_title.replace(' ', '-')
            
            # 更新数据
            cursor.execute("""
                UPDATE animes 
                SET title = %s,
                    title_jp = '',
                    description = %s,
                    cover_image = %s,
                    episodes = %s,
                    status = %s,
                    release_year = %s,
                    release_date = %s,
                    studio = %s,
                    genre = %s,
                    average_rating = %s,
                    rating_count = %s,
                    nationality = %s,
                    anime_type = %s,
                    is_movie = %s,
                    is_hidden_gem = 0
                WHERE id = %s
            """, (
                new_title,
                description,
                f"https://picsum.photos/seed/{title_seed}/300/400",
                episodes,
                status,
                release_year,
                release_date,
                studio,
                genre,
                average_rating,
                rating_count,
                nationality,
                genre,
                is_movie,
                anime_id
            ))
            
            fix_count += 1
            
            if fix_count % batch_size == 0:
                connection.commit()
                print(f"进度: {fix_count:,}/{len(all_animes):,} ({fix_count/len(all_animes)*100:.1f}%)")
        
        # 最后提交
        connection.commit()
        
        print()
        print("=" * 70)
        print(f"最终修复完成！")
        print(f"- B站冷门佳作: {hidden_gem_count} 条")
        print(f"- 修复普通动漫: {fix_count:,} 条")
        print("=" * 70)
        
        # 统计总数
        cursor.execute("SELECT COUNT(*) as total FROM animes")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as gems FROM animes WHERE is_hidden_gem = 1")
        gems = cursor.fetchone()['gems']
        
        print()
        print(f"📊 最终数据库统计:")
        print(f"   总数据: {total:,} 条")
        print(f"   B站冷门佳作: {gems} 条")
        print(f"   普通动漫: {total - gems:,} 条")
        print()
        
        # 展示冷门佳作
        print("🎯 B站冷门佳作列表:")
        cursor.execute("""
            SELECT id, title, description, average_rating, nationality
            FROM animes 
            WHERE is_hidden_gem = 1
            ORDER BY title
        """)
        gems = cursor.fetchall()
        
        for i, gem in enumerate(gems, 1):
            print(f"  {i:2d}. {gem['title']} ({gem['nationality']}) - {gem['average_rating']}分")
            print(f"      {gem['description'][:40]}...")
        
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
