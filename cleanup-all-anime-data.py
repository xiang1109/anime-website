#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面清理和修复所有动漫数据
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

# 好的动漫名称素材库
GOOD_TITLE_WORDS_1 = [
    "星空", "银河", "星辰", "月光", "晨曦", "黄昏", "拂晓", "夜幕",
    "樱花", "枫叶", "雪花", "风花", "紫阳花", "向日葵", "薰衣草", "玫瑰",
    "海洋", "天空", "大地", "森林", "山岳", "河流", "湖泊", "沙漠",
    "传说", "神话", "史诗", "战记", "异闻", "奇谈", "物语", "传奇",
    "冒险", "旅程", "征途", "征程", "探索", "发现", "秘密", "真相",
    "战斗", "战争", "和平", "羁绊", "友情", "爱情", "亲情", "守护",
    "勇者", "英雄", "骑士", "战士", "法师", "贤者", "魔王", "龙",
    "精灵", "妖精", "魔法", "异能", "超能力", "科幻", "机战",
    "校园", "青春", "日常", "喜剧", "治愈", "感动", "热血", "励志",
    "音乐", "艺术", "运动", "竞技", "料理", "美食", "旅行", "游记"
]

GOOD_TITLE_WORDS_2 = [
    "协奏曲", "交响曲", "圆舞曲", "小夜曲", "幻想曲", "狂想曲",
    "王国", "帝国", "共和国", "联邦", "同盟", "公国", "学院", "学园",
    "骑士团", "魔法团", "冒险团", "公会", "家族", "门派", "组织",
    "小队", "分队", "中队", "大队", "军团", "舰队", "战队", "特遣队",
    "冒险者", "探索者", "发现者", "研究者", "学者", "战士", "骑士",
    "学生", "教师", "偶像", "歌手", "演员", "设计师", "画家", "作家",
    "侦探", "刑警", "警察", "医生", "护士", "科学家", "工程师", "厨师",
    "森林", "山脉", "河流", "海洋", "湖泊", "沙漠", "草原", "城市",
    "小镇", "村庄", "学校", "图书馆", "博物馆", "美术馆", "音乐厅",
    "咖啡店", "餐厅", "酒吧", "旅馆", "神社", "寺庙", "教堂", "城堡"
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

def generate_good_title(index):
    """生成合理的、唯一的动漫标题"""
    use_word1 = random.random() < 0.7
    use_word2 = random.random() < 0.6
    
    word1 = random.choice(GOOD_TITLE_WORDS_1) if use_word1 else ""
    word2 = random.choice(GOOD_TITLE_WORDS_2) if use_word2 else random.choice(GOOD_TITLE_WORDS_2)
    
    # 有时候加序号
    suffix = ""
    if random.random() < 0.2:
        season_num = random.randint(1, 4)
        season_names = ["第一季", "第二季", "第三季", "第四季"]
        suffix = " " + season_names[season_num - 1]
    elif random.random() < 0.1:
        suffix = " 特别篇" if random.random() < 0.5 else " 剧场版"
    
    title = f"{word1}{word2}{suffix}".strip()
    
    # 确保标题不重复（必须使用index）
    title = f"{title} {index}"
    
    return title

def main():
    """主函数"""
    print("=" * 70)
    print("全面清理和修复所有动漫数据")
    print("=" * 70)
    print()
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
        print()
        
        cursor = connection.cursor(dictionary=True)
        
        # 先统计一下总数据量
        cursor.execute("SELECT COUNT(*) as total FROM animes")
        total = cursor.fetchone()['total']
        print(f"当前数据库总数据: {total:,} 条")
        print()
        
        # 获取所有需要修复的ID
        cursor.execute("SELECT id, title FROM animes ORDER BY id")
        all_animes = cursor.fetchall()
        
        print(f"开始修复 {len(all_animes):,} 条数据...")
        print()
        
        fix_count = 0
        batch_size = 100
        
        for i, anime in enumerate(all_animes):
            anime_id = anime['id']
            old_title = anime['title']
            
            # 检查标题是否需要修复（包含奇怪的数字或格式）
            needs_fix = False
            if ' ' in old_title and any(c.isdigit() for c in old_title.split()[-1]):
                # 标题末尾有数字，可能需要修复
                needs_fix = True
            if len(old_title) > 30:
                needs_fix = True
            if any(bad in old_title for bad in ['  ', '  ', '  ', '卷', '册', '本']):
                needs_fix = True
            
            # 随机修复一些（或者全部修复）
            if True or needs_fix:
                # 生成新的合理标题
                new_title = generate_good_title(i)
                
                # 确保不重复（简单处理）
                new_title = f"{new_title} {i}" if random.random() < 0.05 else new_title
                
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
                
                # 封面图片使用标题作为seed，去掉空格
                title_seed = new_title.replace(' ', '-').replace('！', '').replace('·', '')
                
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
                        is_movie = %s
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
                
                if fix_count % 500 == 0:
                    print(f"  最新: {old_title[:30]}... → {new_title}")
        
        # 最后提交
        connection.commit()
        
        print()
        print("=" * 70)
        print(f"数据全面修复完成！")
        print(f"成功修复: {fix_count:,} 条动漫数据")
        print("=" * 70)
        
        # 展示修复后的例子
        print()
        print("📌 修复后的作品示例:")
        cursor.execute("""
            SELECT id, title, description, cover_image, release_year, episodes, 
                   average_rating, rating_count, nationality, status, studio, genre
            FROM animes 
            ORDER BY id DESC 
            LIMIT 20
        """)
        examples = cursor.fetchall()
        
        for i, anime in enumerate(examples, 1):
            print(f"\n{i}. {anime['title']}")
            print(f"   年份: {anime['release_year']} | 集数: {anime['episodes']} | 评分: {anime['average_rating']} | {anime['status']}")
            print(f"   制作: {anime['studio']} | 类型: {anime['genre']} | 国籍: {anime['nationality']}")
            print(f"   评价: {anime['rating_count']:,}人")
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
