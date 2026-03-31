#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成大量动漫数据脚本
生成5000条以上的动漫数据插入到数据库
"""

import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta
import string

# 数据库配置
DB_CONFIG = {
    'host': '59.110.214.50',
    'port': 3306,
    'user': 'anime_user',
    'password': 'Xinmima1109',
    'database': 'anime_db',
    'charset': 'utf8mb4'
}

# 动漫数据素材库
ANIME_TITLES_CN = [
    "进击的巨人", "鬼灭之刃", "咒术回战", "间谍过家家", "我推的孩子",
    "辉夜大小姐想让我告白", "灵能百分百", "我的青春恋爱物语果然有问题",
    "关于我转生变成史莱姆这档事", "无职转生", "Re:从零开始的异世界生活",
    "为美好的世界献上祝福", "刀剑神域", "进击的巨人 最终季", "鬼灭之刃 无限列车篇",
    "鬼灭之刃 锻刀村篇", "鬼灭之刃 柱训练篇", "咒术回战 第二季",
    "咒术回战 怀玉·玉折", "间谍过家家 第二季", "我推的孩子 第二季",
    "辉夜大小姐想让我告白 第四季", "灵能百分百 第三季", "葬送的芙莉莲",
    "迷宫饭", "药屋少女的呢喃", "怪兽8号", "国王排名", "鲁邦三世",
    "名侦探柯南", "海贼王", "火影忍者", "龙珠超", "银魂",
    "全职猎人", "家庭教师", "妖精的尾巴", "死神", "美食的俘虏",
    "黑色五叶草", "我的英雄学院", "排球少年", "强风吹拂", "乒乓",
    "钻石王牌", "网球王子", "新网球王子", "灌篮高手", "排球少年！！",
    "蓝色监狱", "青之芦苇", "足球小将", "棒球大联盟", "头文字D",
    "极速车魂", "高智能方程式", "新世纪福音战士", "星际牛仔", "混沌武士",
    "攻壳机动队", "阿基拉", "天空之城", "龙猫", "千与千寻",
    "哈尔的移动城堡", "幽灵公主", "风之谷", "起风了", "悬崖上的金鱼姬",
    "借东西的小人阿莉埃蒂", "记忆中的玛妮", "你想活出怎样的人生", "铃芽之旅",
    "天气之子", "你的名字", "秒速五厘米", "言叶之庭", "云之彼端，约定的地方",
    "追逐繁星的孩子", "星之声", "她和她的猫", "十字路口", "某人的目光",
    "猫的集会", "Planetes", "星空清理者", "月光之旅", "宇宙兄弟",
    "彼方的阿斯特拉", "Dr.STONE 新石纪", "来自深渊", "来自新世界",
    "约定的梦幻岛", "战栗杀机", "Banana Fish", "91天", "黑街",
    "GANGSTA匪徒", "血界战线", "幻界战线", "最游记", "最游记RELOAD",
    "最游记RELOAD GUNLOCK", "最游记RELOAD ZEROIN", "最游记RELOAD BLAST",
    "最游记RELOAD -ZEROIN-", "最游记RELOAD -ZEROIN-", "最游记RELOAD -ZEROIN-",
    "最游记RELOAD -ZEROIN-", "最游记RELOAD -ZEROIN-", "最游记RELOAD -ZEROIN-"
]

ANIME_TITLES_JP = [
    "進撃の巨人", "鬼滅の刃", "呪術廻戦", "SPY×FAMILY", "推しの子",
    "かぐや様は告らせたい", "モブサイコ100", "やはり俺の青春ラブコメはまちがっている",
    "転生したらスライムだった件", "無職転生", "Re:ゼロから始める異世界生活",
    "この素晴らしい世界に祝福を！", "ソードアート・オンライン", "進撃の巨人 The Final Season",
    "鬼滅の刃 無限列車編", "鬼滅の刃 刀鍛冶の里編", "鬼滅の刃 柱稽古編",
    "呪術廻戦 第2期", "呪術廻戦 懐玉・玉折", "SPY×FAMILY 第2期",
    "推しの子 第2期", "かぐや様は告らせたい 第4期", "モブサイコ100 III",
    "葬送のフリーレン", "ダンジョン飯", "薬屋のひとりごと", "怪獣8号",
    "王様ランキング", "ルパン三世", "名探偵コナン", "ONE PIECE",
    "NARUTO - ナルト", "ドラゴンボール超", "銀魂", "HUNTER×HUNTER",
    "家庭教師ヒットマンREBORN!", "FAIRY TAIL", "BLEACH", "トリコ",
    "ブラッククローバー", "僕のヒーローアカデミア", "ハイキュー!!", "風が強く吹いている",
    "ピンポン", "ダイヤのA", "テニスの王子様", "新テニスの王子様", "SLAM DUNK",
    "ブルーロック", "アオアシ", "キャプテン翼", "メジャー", "頭文字D",
    "MFゴースト", "新世紀GPXサイバーフォーミュラ", "新世紀エヴァンゲリオン",
    "カウボーイビバップ", "サムライチャンプルー", "攻殻機動隊", "AKIRA",
    "天空の城ラピュタ", "となりのトトロ", "千と千尋の神隠し", "ハウルの動く城",
    "もののけ姫", "風の谷のナウシカ", "風立ちぬ", "崖の上のポニョ",
    "借りぐらしのアリエッティ", "思い出のマーニー", "君たちはどう生きるか", "すずめの戸締まり",
    "天気の子", "君の名は。", "秒速5センチメートル", "言の葉の庭",
    "雲のむこう、約束の場所", "星を追う子ども", "ほしのこえ", "彼女と彼女の猫",
    "クロスロード", "だれかのまなざし", "猫の集会", "プラネテス",
    "星空のクリアラー", "月光のミッドナイト", "宇宙兄弟", "彼方のアストラ",
    "Dr.STONE", "メイドインアビス", "新世界より", "約束のネバーランド",
    "BANANA FISH", "91Days", "GANGSTA.", "血界戦線",
    "幻界戦線", "最遊記", "最遊記RELOAD", "最遊記RELOAD GUNLOCK"
]

DESCRIPTIONS = [
    "讲述了一个关于勇气与友情的精彩故事，主角在逆境中不断成长，最终实现了自己的梦想。",
    "在奇幻的异世界中，主角与伙伴们一起展开了一场惊心动魄的冒险之旅。",
    "一部充满悬疑与推理的作品，每一个情节都让人紧张不已，结局更是出人意料。",
    "描绘了青春期少年少女们的纯真爱情故事，甜蜜中带着一丝苦涩。",
    "热血沸腾的战斗场面，精美绝伦的动画制作，让人看了热血澎湃。",
    "治愈系作品，温馨的画面和动人的故事，让人感受到生活的美好。",
    "科幻巨作，讲述了未来世界的人类与科技的关系，引人深思。",
    "历史题材作品，还原了那个波澜壮阔的时代，让人身临其境。",
    "校园喜剧，充满了欢声笑语，让人在繁忙的生活中得到放松。",
    "体育竞技作品，展现了运动员们的拼搏精神和对梦想的执着追求。"
]

STUDIOS = [
    "Madhouse", "ufotable", "MAPPA", "WIT STUDIO", "京都动画",
    "动画工房", "Production I.G", "A-1 Pictures", "CloverWorks", "BONES",
    "SHAFT", "J.C.STAFF", "日升动画", "东映动画", "OLM Team Kato",
    "Studio DEEN", "Studio 5组", "ZEXCS", "feel.", "SILVER LINK.",
    "TRIGGER", "P.A.WORKS", "WHITE FOX", "8bit", "Lay-duce",
    "TROYCA", "C2C", "Nexus", "EMT Squared", "project No.9",
    "Millepensee", "TYO Animations", "动画工房", "AIC", "Seven Arcs",
    "Satelight", "AQUAPLUS", "TYO Animations", "Bridge", "Gallop",
    "手冢Production", "MADHOUSE", "XEBEC", "Studio Ghibli", "科乐美",
    "Production I.G", "龙之子", "NAS", "亚细亚堂", "Mook DLE"
]

ANIME_TYPES = [
    "热血", "奇幻", "冒险", "悬疑", "科幻", "爱情", "喜剧",
    "运动", "治愈", "历史", "战争", "恐怖", "推理", "机战",
    "日常", "校园", "职场", "偶像", "音乐", "美术", "料理"
]

NATIONALITIES = ["日本", "中国", "韩国", "美国", "法国", "德国", "英国", "意大利", "西班牙", "加拿大"]

STATUSES = ["连载中", "已完结", "未播出"]

def generate_random_title():
    """生成随机标题"""
    base_title = random.choice(ANIME_TITLES_CN)
    suffixes = ["", " 特别篇", " 最终季", " 第二季", " 第三季", " 第四季", 
                " 剧场版", " OVA", " 新作", " 重制版", " 重置版"]
    suffix = random.choice(suffixes)
    
    # 添加随机编号
    if random.random() < 0.3:
        numbers = [" I", " II", " III", " IV", " V", " VI", " VII", " VIII", " IX", " X"]
        suffix += random.choice(numbers)
    
    return base_title + suffix

def generate_random_jp_title(cn_title):
    """根据中文标题生成日文标题"""
    for i, cn in enumerate(ANIME_TITLES_CN):
        if cn in cn_title and i < len(ANIME_TITLES_JP):
            return ANIME_TITLES_JP[i]
    return ""

def generate_anime_data(index):
    """生成单条动漫数据"""
    title = generate_random_title()
    title_jp = generate_random_jp_title(title)
    
    # 随机年份（2015-2026）
    release_year = random.randint(2015, 2026)
    
    # 随机日期
    if release_year == 2026:
        month = random.randint(1, 3)
    else:
        month = random.randint(1, 12)
    day = random.randint(1, 28)
    release_date = f"{release_year}-{month:02d}-{day:02d}"
    
    # 随机集数
    episodes = random.randint(1, 100) if random.random() > 0.2 else random.randint(1, 24)
    
    # 随机评分和评分人数
    average_rating = round(random.uniform(5.0, 9.8), 2)
    rating_count = random.randint(1000, 300000)
    
    # 随机状态
    status = random.choices(STATUSES, weights=[0.4, 0.5, 0.1])[0]
    
    # 是否是剧场版
    is_movie = 1 if random.random() < 0.15 else 0
    if is_movie:
        episodes = random.randint(0, 3)
        status = "已完结"
    
    return {
        'title': title,
        'title_jp': title_jp,
        'description': random.choice(DESCRIPTIONS),
        'cover_image': f"https://picsum.photos/seed/anime{index}/300/400",
        'episodes': episodes,
        'status': status,
        'release_year': release_year,
        'release_date': release_date,
        'studio': random.choice(STUDIOS),
        'genre': random.choice(ANIME_TYPES),
        'average_rating': average_rating,
        'rating_count': rating_count,
        'nationality': random.choices(NATIONALITIES, weights=[0.7, 0.15, 0.05, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01])[0],
        'anime_type': random.choice(ANIME_TYPES),
        'is_movie': is_movie
    }

def insert_anime_data(connection, anime_data):
    """插入单条动漫数据"""
    try:
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO animes 
        (title, title_jp, description, cover_image, episodes, status,
         release_year, release_date, studio, genre, average_rating, rating_count,
         nationality, anime_type, is_movie, created_at)
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
        
        return True
    except Error as e:
        print(f"插入错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("生成大量动漫数据脚本")
    print("=" * 70)
    print()
    
    # 生成数量
    TOTAL_ANIMES = 5500  # 生成5500条数据
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
        print()
        
        print(f"开始生成 {TOTAL_ANIMES} 条动漫数据...")
        print()
        
        success_count = 0
        batch_size = 100
        
        for i in range(TOTAL_ANIMES):
            anime_data = generate_anime_data(i + 1)
            
            if insert_anime_data(connection, anime_data):
                success_count += 1
                
                # 每100条提交一次并显示进度
                if (i + 1) % batch_size == 0:
                    connection.commit()
                    print(f"进度: {i + 1}/{TOTAL_ANIMES} ({(i + 1) / TOTAL_ANIMES * 100:.1f}%)")
                
                # 每1000条显示一次详细信息
                if (i + 1) % 1000 == 0:
                    print(f"  最近一条: {anime_data['title']} ({anime_data['release_year']})")
        
        # 最后提交
        connection.commit()
        
        print()
        print("=" * 70)
        print(f"数据生成完成！")
        print(f"成功插入: {success_count} 条动漫数据")
        print("=" * 70)
        
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
