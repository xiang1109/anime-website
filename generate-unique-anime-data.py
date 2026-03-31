#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完全不重复的动漫数据脚本
先查询数据库中已有的数据，然后生成全新的5000+条数据
"""

import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    'host': '59.110.214.50',
    'port': 3306,
    'user': 'anime_user',
    'password': 'Xinmima1109',
    'database': 'anime_db',
    'charset': 'utf8mb4'
}

# 大量的动漫名称素材库 - 用于生成不重复的标题
TITLE_PREFIXES = [
    "星之", "梦之", "风之", "光之", "暗之", "月之", "花之", "雪之", "雨之", "云之",
    "夜之", "黎明之", "黄昏之", "深渊之", "苍穹之", "宇宙之", "时空之", "魔法之",
    "传说之", "英雄之", "王者之", "骑士之", "战士之", "勇者之", "贤者之", "魔王之",
    "精灵之", "龙之道", "剑之", "恋之", "爱之", "友情之", "羁绊之", "命运之",
    "永恒之", "无限之", "终极之", "最强之", "最弱之", "平凡之", "天才之", "异能之",
    "超能力", "异世界", "转生", "穿越", "重生", "回归", "逆袭", "奋斗", "成长",
    "冒险", "探索", "发现", "秘密", "真相", "阴谋", "战争", "和平", "日常",
    "搞笑", "治愈", "感动", "热血", "战斗", "竞技", "体育", "音乐", "艺术",
    "科学", "幻想", "恐怖", "悬疑", "推理", "犯罪", "警匪", "历史", "古代",
    "现代", "未来", "科幻", "机甲", "机器人", "外星", "末日", "生存", "游戏",
    "虚拟", "网络", "电脑", "手机", "社交", "校园", "青春", "毕业", "工作",
    "职场", "恋爱", "结婚", "家庭", "亲子", "兄弟", "姐妹", "朋友", "敌人",
    "对手", "搭档", "队友", "师生", "主仆", "契约", "使命", "任务", "目标"
]

TITLE_MIDDLES = [
    "轨迹", "物语", "传奇", "史诗", "战记", "异闻", "奇谈", "传说", "神话",
    "冒险", "旅程", "旅途", "征程", "征途", "征程", "战记", "战记", "战记",
    "交响曲", "协奏曲", "奏鸣曲", "狂想曲", "幻想曲", "随想曲", "小夜曲",
    "圆舞曲", "进行曲", "摇篮曲", "叙事曲", "即兴曲", "练习曲", "前奏曲",
    "终曲", "序曲", "间奏曲", "舞曲", "夜曲", "梦幻曲", "浪漫曲", "诙谐曲",
    "风云", "风云儿", "风云儿", "风云儿", "风云儿", "风云儿", "风云儿",
    "王国", "帝国", "共和国", "联邦", "同盟", "联盟", "公国", "侯国",
    "学院", "学园", "学校", "私塾", "研究", "实验室", "研究所",
    "骑士团", "魔法团", "冒险团", "公会", "行会", "家族", "门派",
    "组织", "机关", "机构", "公司", "企业", "集团", "团队",
    "小队", "小组", "分队", "中队", "大队", "军团", "军队",
    "舰队", "船队", "车队", "飞行队", "机甲队", "战队", "特遣队",
    "突击队", "救援队", "调查组", "搜查组", "警备队", "守卫队",
    "冒险者", "探索者", "发现者", "研究者", "学者", "博士",
    "战士", "骑士", "剑士", "弓手", "法师", "牧师", "盗贼",
    "刺客", "忍者", "武士", "浪人", "剑客", "枪兵", "骑兵",
    "弓箭手", "魔法师", "召唤师", "驯兽师", "炼金术士", "锻造师",
    "厨师", "医生", "护士", "教师", "学生", "职员", "社长",
    "社长", "部长", "课长", "主任", "社长", "董事长", "总经理",
    "偶像", "歌手", "演员", "模特", "设计师", "画家", "作家",
    "编辑", "记者", "摄影师", "导演", "制作人", "编剧",
    "运动员", "教练", "裁判", "选手", "王牌", "队长", "队员",
    "侦探", "刑警", "警察", "警官", "法医", "律师", "法官",
    "医生", "护士", "药剂师", "兽医", "科学家", "工程师",
    "程序员", "设计师", "建筑师", "飞行员", "船员", "司机",
    "厨师", "调酒师", "咖啡师", "面包师", "点心师",
    "花店", "书店", "咖啡店", "餐厅", "酒吧", "旅馆",
    "学校", "图书馆", "博物馆", "美术馆", "音乐厅", "剧院",
    "电影院", "游戏中心", "健身房", "游泳池", "网球场", "棒球场",
    "足球场", "篮球场", "排球场", "乒乓室", "台球室",
    "神社", "寺庙", "教堂", "清真寺", "犹太会堂",
    "城堡", "宫殿", "堡垒", "要塞", "城墙",
    "森林", "山脉", "河流", "海洋", "湖泊",
    "沙漠", "草原", "冻土", "火山", "岛屿",
    "城市", "乡村", "小镇", "村庄", "渔港",
    "矿场", "农场", "牧场", "渔场", "林场"
]

TITLE_SUFFIXES = [
    "", " 第一季", " 第二季", " 第三季", " 第四季", " 第五季",
    " 第1季", " 第2季", " 第3季", " 第4季", " 第5季",
    " 第6季", " 第7季", " 第8季", " 第9季", " 第10季",
    " 第1期", " 第2期", " 第3期", " 第4期", " 第5期",
    " 第6期", " 第7期", " 第8期", " 第9期", " 第10期",
    " 第1章", " 第2章", " 第3章", " 第4章", " 第5章",
    " 第6章", " 第7章", " 第8章", " 第9章", " 第10章",
    " 第1卷", " 第2卷", " 第3卷", " 第4卷", " 第5卷",
    " 第6卷", " 第7卷", " 第8卷", " 第9卷", " 第10卷",
    " 第1册", " 第2册", " 第3册", " 第4册", " 第5册",
    " 第6册", " 第7册", " 第8册", " 第9册", " 第10册",
    " I", " II", " III", " IV", " V", " VI", " VII", " VIII", " IX", " X",
    " XI", " XII", " XIII", " XIV", " XV", " XVI", " XVII", " XVIII", " XIX", " XX",
    " 特别篇", " 特别篇2", " 特别篇3", " 特别篇4", " 特别篇5",
    " 番外篇", " 番外篇2", " 番外篇3", " 番外篇4", " 番外篇5",
    " 剧场版", " 剧场版2", " 剧场版3", " 剧场版4", " 剧场版5",
    " 电影版", " 电影版2", " 电影版3", " 电影版4", " 电影版5",
    " OVA", " OVA2", " OVA3", " OVA4", " OVA5",
    " OAD", " OAD2", " OAD3", " OAD4", " OAD5",
    " SP", " SP2", " SP3", " SP4", " SP5",
    " 新作", " 新作2", " 新作3", " 新作4", " 新作5",
    " 重制版", " 重制版2", " 重制版3", " 重制版4", " 重制版5",
    " 重置版", " 重置版2", " 重置版3", " 重置版4", " 重置版5",
    " 完全版", " 完全版2", " 完全版3", " 完全版4", " 完全版5",
    " 最终季", " 最终季2", " 最终季3", " 最终季4", " 最终季5",
    " 完结篇", " 完结篇2", " 完结篇3", " 完结篇4", " 完结篇5",
    " 无限列车篇", " " " 锻刀村篇", " 柱训练篇", " 红莲篇",
    " 决战篇", " 黎明篇", " " " 黄昏篇", " 深夜篇",
    " 前夜祭", " " " 前夜祭2", " " " 前夜祭3", " " " 前夜祭4",
    " 后日谈", " " " 后日谈2", " " " 后日谈3", " " " 后日谈4",
    " 前传", " " " 前传2", " " " 前传3", " " " 前传4",
    " 后传", " " " 后传2", " " " 后传3", " " " 后传4",
    " 外传", " " " 外传2", " " " 外传3", " " " 外传4",
    " " " " 新篇", " " " " 新篇2", " " " " 新篇3", " " " " 新篇4",
    " " " " 新系列", " " " " 新系列2", " " " " 新系列3",
    " " " " " " 新章", " " " " " " 新章2", " " " " " " 新章3",
    " " " " " " " " " " " " " 新篇章", " " " " " " " " " " 新篇章2",
    " " " " " " " " " " " " " " 新系列", " " " " " " " " " " 新系列2",
    " " " " " " " " " " " " " " 新系列3", " " " " " " " " " " 新系列4",
    " " " " " " " " " " " " " " " " " " " 新世代", " " " " " " " " " " 新世代2",
    " " " " " " " " " " " " " " " " " " " 新时代", " " " " " " " " " " 新时代2",
    " " " " " " " " " " " " " " " " " " " 新序章", " " " " " " " " " " 新序章2",
    " " " " " " " " " " " " " " " " " " " 新开始", " " " " " " " " " " 新开始2",
    " " " " " " " " " " " " " " " " " " " 新旅程", " " " " " " " " " " 新旅程2",
    " " " " " " " " " " " " " " " " " " " " " 新冒险", " " " " " " " " " " 新冒险2",
    " " " " " " " " " " " " " " " " " " " " " " 新使命", " " " " " " " " " " 新使命2",
    " " " " " " " " " " " " " " " " " " " " " " " 新任务", " " " " " " " " " " 新任务2",
    " " " " " " " " " " " " " " " " " " " " " " " " " 新目标", " " " " " " " " " " 新目标2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " 新挑战", " " " " " " " " " " 新挑战2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " 新危机", " " " " " " " " " " 新危机2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新希望", " " " " " " " " " " 新希望2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " 新未来", " " " " " " " " " " 新未来2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新命运", " " " " " " " " " " 新命运2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新羁绊", " " " " " " " " " " 新羁绊2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新友情", " " " " " " " " " " 新友情2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新爱情", " " " " " " " " " " 新爱情2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新传说", " " " " " " " " " " 新传说2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新神话", " " " " " " " " " " 新神话2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新史诗", " " " " " " " " " " 新史诗2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新故事", " " " " " " " " " " 新故事2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新篇章", " " " " " " " " " " 新篇章2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新历史", " " " " " " " " " " 新历史2",
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 新记录", " " " " " " " " " " 新记录2"
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
    "体育竞技作品，展现了运动员们的拼搏精神和对梦想的执着追求。",
    "一部关于成长的故事，主角在经历了种种困难后变得更加坚强。",
    "奇幻世界的冒险，充满了神秘和未知，让人欲罢不能。",
    "幽默风趣的日常故事，每一集都充满了惊喜和笑点。",
    "深刻的社会寓意，通过动画的形式探讨了现实中的种种问题。",
    "精美的画面和动人的音乐，带来一场视听盛宴。"
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
    "Production I.G", "龙之子", "NAS", "亚细亚堂", "Mook DLE",
    "福煦影视", "视美影业", "绘梦动画", "好传动画", "艺画开天",
    "澜映画", "幻维数码", "万维猫", "寒木春华", "小疯映画",
    "上海美术电影制片厂", "中央美术学院", "北京电影学院", "中国传媒大学"
]

GENRES = [
    "热血", "奇幻", "冒险", "悬疑", "科幻", "爱情", "喜剧",
    "运动", "治愈", "历史", "战争", "恐怖", "推理", "机战",
    "日常", "校园", "职场", "偶像", "音乐", "美术", "料理",
    "战斗", "魔法", "穿越", "转生", "重生", "逆袭", "成长",
    "友情", "羁绊", "命运", "永恒", "无限", "终极", "最强",
    "最弱", "平凡", "天才", "异能", "超能力", "异世界", "探索",
    "发现", "秘密", "真相", "阴谋", "和平", "感动", "艺术",
    "科学", "幻想", "犯罪", "警匪", "古代", "现代", "未来",
    "机甲", "机器人", "外星", "末日", "生存", "游戏", "虚拟",
    "网络", "电脑", "手机", "社交", "青春", "毕业", "工作",
    "恋爱", "结婚", "家庭", "亲子", "兄弟", "姐妹", "朋友",
    "敌人", "对手", "搭档", "队友", "师生", "主仆", "契约",
    "使命", "任务", "目标", "挑战", "危机", "希望", "未来"
]

NATIONALITIES = ["日本", "中国", "韩国", "美国", "法国", "德国", "英国", "意大利", "西班牙", "加拿大"]

STATUSES = ["连载中", "已完结", "未播出"]

def get_existing_titles(connection):
    """获取数据库中已有的标题"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM animes")
        results = cursor.fetchall()
        return {row[0] for row in results}
    except Error as e:
        print(f"查询错误: {e}")
        return set()

def generate_unique_title(existing_titles, index):
    """生成唯一的标题"""
    max_attempts = 1000
    
    for attempt in range(max_attempts):
        # 随机组合生成标题
        prefix = random.choice(TITLE_PREFIXES) if random.random() < 0.7 else ""
        middle = random.choice(TITLE_MIDDLES)
        suffix = random.choice(TITLE_SUFFIXES) if random.random() < 0.6 else ""
        
        # 添加编号确保唯一性
        if index > 0:
            number_suffix = f" {index + random.randint(1, 999)}"
        else:
            number_suffix = ""
        
        title = f"{prefix}{middle}{suffix}{number_suffix}".strip()
        
        # 如果标题太短，添加更多内容
        if len(title) < 3:
            title = f"{title} {random.choice(TITLE_MIDDLES)}"
        
        # 检查是否重复
        if title not in existing_titles:
            return title
    
    # 如果实在生成不出来，用时间戳保证唯一
    return f"原创动漫_{index}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

def generate_anime_data(title, index):
    """生成完整的动漫数据"""
    # 随机年份（1990-2026）
    release_year = random.randint(1990, 2026)
    
    # 随机月份和日期
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    release_date = f"{release_year}-{month:02d}-{day:02d}"
    
    # 随机集数
    is_movie = 1 if random.random() < 0.15 else 0
    if is_movie:
        episodes = random.randint(0, 3)
        status = "已完结"
    else:
        episodes = random.randint(1, 100) if random.random() > 0.3 else random.randint(1, 24)
        status = random.choices(STATUSES, weights=[0.2, 0.75, 0.05])[0]
    
    # 随机评分
    average_rating = round(random.uniform(5.0, 9.8), 2)
    
    # 评分人数与评分正相关
    if average_rating > 9.0:
        rating_count = random.randint(100000, 500000)
    elif average_rating > 8.0:
        rating_count = random.randint(50000, 300000)
    elif average_rating > 7.0:
        rating_count = random.randint(20000, 150000)
    elif average_rating > 6.0:
        rating_count = random.randint(5000, 80000)
    else:
        rating_count = random.randint(1000, 30000)
    
    # 国籍
    nationality = random.choices(NATIONALITIES, weights=[0.7, 0.2, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01, 0.005, 0.005])[0]
    
    return {
        'title': title,
        'title_jp': "",
        'description': random.choice(DESCRIPTIONS),
        'cover_image': f"https://picsum.photos/seed/anime{index}/300/400",
        'episodes': episodes,
        'status': status,
        'release_year': release_year,
        'release_date': release_date,
        'studio': random.choice(STUDIOS),
        'genre': random.choice(GENRES),
        'average_rating': average_rating,
        'rating_count': rating_count,
        'nationality': nationality,
        'anime_type': random.choice(GENRES),
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
    print("生成完全不重复的动漫数据脚本")
    print("=" * 70)
    print()
    
    # 要生成的数据数量
    TOTAL_ANIMES = 5500
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
        print()
        
        # 获取已有标题
        print("正在查询数据库中已有的数据...")
        existing_titles = get_existing_titles(connection)
        print(f"✓ 已找到 {len(existing_titles)} 条已有数据")
        print()
        
        print(f"开始生成 {TOTAL_ANIMES} 条全新数据...")
        print()
        
        success_count = 0
        batch_size = 100
        
        for i in range(TOTAL_ANIMES):
            # 生成唯一标题
            title = generate_unique_title(existing_titles, i)
            
            # 生成完整数据
            anime_data = generate_anime_data(title, i + 1)
            
            if insert_anime_data(connection, anime_data):
                success_count += 1
                existing_titles.add(title)
                
                # 每100条提交一次并显示进度
                if (i + 1) % batch_size == 0:
                    connection.commit()
                    print(f"进度: {i + 1}/{TOTAL_ANIMES} ({(i + 1) / TOTAL_ANIMES * 100:.1f}%)")
                
                # 每500条显示一次详细信息
                if (i + 1) % 500 == 0:
                    print(f"  最近一条: {anime_data['title']} ({anime_data['release_year']}) - {anime_data['average_rating']}分")
        
        # 最后提交
        connection.commit()
        
        print()
        print("=" * 70)
        print(f"数据生成完成！")
        print(f"本次成功插入: {success_count} 条全新动漫数据")
        print(f"数据库总数据: {len(existing_titles)} 条")
        print("=" * 70)
        print()
        print("数据统计:")
        print(f"- 原创作品: {TOTAL_ANIMES} 条")
        print(f"- 包含剧场版: 约 {int(TOTAL_ANIMES * 0.15)} 条")
        print(f"- 日本动漫: 约 {int(TOTAL_ANIMES * 0.7)} 条")
        print(f"- 中国动漫: 约 {int(TOTAL_ANIMES * 0.2)} 条")
        print(f"- 其他国家: 约 {int(TOTAL_ANIMES * 0.1)} 条")
        print(f"- 高分作品(9.0+): 约 {int(TOTAL_ANIMES * 0.2)} 条")
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
