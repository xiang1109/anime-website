import pymysql
from datetime import datetime
import random

def generate_real_anime_data():
    real_anime_list = [
        {"title": "进击的巨人", "title_jp": "進撃の巨人", "description": "在一个人类被巨人捕食的世界中，主角艾伦·耶格尔加入调查兵团与巨人战斗，揭开巨人的秘密和人类的历史。", "episodes": 87, "status": "完结", "release_year": 2013, "studio": "Wit Studio", "genre": "动作,冒险,奇幻", "average_rating": 9.5, "rating_count": 1500000},
        {"title": "海贼王", "title_jp": "ONE PIECE", "description": "蒙奇·D·路飞带领草帽海贼团寻找传说中的One Piece，在伟大航路上展开冒险，结交伙伴，挑战强敌。", "episodes": 1100, "status": "连载中", "release_year": 1999, "studio": "东映动画", "genre": "动作,冒险,奇幻", "average_rating": 9.2, "rating_count": 2000000},
        {"title": "火影忍者", "title_jp": "NARUTO", "description": "关于忍者鸣人的成长故事，从被排斥的孤儿到拯救世界的英雄，讲述友情、努力和胜利的故事。", "episodes": 720, "status": "完结", "release_year": 2002, "studio": "Studio Pierrot", "genre": "动作,冒险,奇幻", "average_rating": 8.9, "rating_count": 1800000},
        {"title": "鬼灭之刃", "title_jp": "鬼滅の刃", "description": "炭治郎为了拯救变成鬼的妹妹祢豆子，加入鬼杀队与恶鬼战斗，揭开鬼的秘密和家族的仇恨。", "episodes": 55, "status": "连载中", "release_year": 2019, "studio": "ufotable", "genre": "动作,冒险,奇幻", "average_rating": 9.1, "rating_count": 1200000},
        {"title": "咒术回战", "title_jp": "呪術廻戦", "description": "虎杖悠仁为了拯救同学，吞下了特级咒物两面宿傩的手指，从此与宿傩共存，加入咒术高专学习咒术。", "episodes": 47, "status": "连载中", "release_year": 2020, "studio": "MAPPA", "genre": "动作,超自然,奇幻", "average_rating": 8.8, "rating_count": 900000},
        {"title": "东京食尸鬼", "title_jp": "東京喰種", "description": "金木研变成半人半食尸鬼的故事，挣扎在人类和食尸鬼两个世界之间，寻找自己的身份和生存的意义。", "episodes": 48, "status": "完结", "release_year": 2014, "studio": "Studio Pierrot", "genre": "动作,恐怖,超自然", "average_rating": 8.3, "rating_count": 800000},
        {"title": "我的英雄学院", "title_jp": "僕のヒーローアカデミア", "description": "绿谷出久在没有个性的情况下，继承了欧尔麦特的One For All，进入雄英高中学习成为英雄的故事。", "episodes": 138, "status": "连载中", "release_year": 2016, "studio": "Bones", "genre": "动作,校园,超能力", "average_rating": 8.5, "rating_count": 950000},
        {"title": "刀剑神域", "title_jp": "ソードアート・オンライン", "description": "桐人被困在虚拟现实游戏刀剑神域中，必须通关100层才能离开，在游戏中结识伙伴，与敌人战斗。", "episodes": 96, "status": "完结", "release_year": 2012, "studio": "A-1 Pictures", "genre": "动作,冒险,游戏", "average_rating": 8.1, "rating_count": 1100000},
        {"title": "名侦探柯南", "title_jp": "名探偵コナン", "description": "高中生侦探工藤新一被黑衣组织灌下毒药后变成小学生，化名江户川柯南，继续解决各种案件，寻找恢复身体的方法。", "episodes": 1100, "status": "连载中", "release_year": 1996, "studio": "TMS Entertainment", "genre": "悬疑,推理,犯罪", "average_rating": 8.7, "rating_count": 2500000},
        {"title": "死亡笔记", "title_jp": "DEATH NOTE", "description": "天才高中生夜神月捡到了可以杀人的死亡笔记，开始清除罪犯，试图创造一个没有犯罪的理想世界，与L展开智力对决。", "episodes": 37, "status": "完结", "release_year": 2006, "studio": "Madhouse", "genre": "悬疑,推理,心理", "average_rating": 9.0, "rating_count": 1500000},
        {"title": "钢之炼金术师", "title_jp": "鋼の錬金術師", "description": "爱德华和阿尔冯斯兄弟为了复活母亲，进行了人体炼成，失去了身体，之后踏上寻找贤者之石的旅程。", "episodes": 64, "status": "完结", "release_year": 2009, "studio": "Bones", "genre": "动作,冒险,奇幻", "average_rating": 9.3, "rating_count": 1200000},
        {"title": "全职猎人", "title_jp": "HUNTER×HUNTER", "description": "小杰为了寻找父亲，踏上成为猎人的旅程，结识奇犽、酷拉皮卡和雷欧力，共同面对各种挑战和敌人。", "episodes": 148, "status": "完结", "release_year": 2011, "studio": "Madhouse", "genre": "动作,冒险,奇幻", "average_rating": 9.2, "rating_count": 1300000},
        {"title": "银魂", "title_jp": "銀魂", "description": "在天人入侵的江户，万事屋的坂田银时和伙伴们过着荒诞的生活，处理各种奇怪的委托，面对各种搞笑和感人的故事。", "episodes": 367, "status": "完结", "release_year": 2006, "studio": "日升动画", "genre": "动作,喜剧,科幻", "average_rating": 8.9, "rating_count": 1100000},
        {"title": "进击的巨人 最终季", "title_jp": "進撃の巨人 The Final Season", "description": "艾伦·耶格尔揭开了巨人的真相，开始了对马莱的复仇，最终导致了世界末日般的战斗，帕拉迪岛和马莱的最终决战。", "episodes": 35, "status": "完结", "release_year": 2020, "studio": "MAPPA", "genre": "动作,冒险,奇幻", "average_rating": 9.6, "rating_count": 1000000},
        {"title": "排球少年", "title_jp": "ハイキュー!!", "description": "日向翔阳因为身高被嘲笑，但他通过努力和队友的配合，在排球场上追逐梦想，展现排球的魅力和团队的力量。", "episodes": 85, "status": "完结", "release_year": 2014, "studio": "Production I.G", "genre": "运动,校园,青春", "average_rating": 8.8, "rating_count": 850000},
        {"title": "黑色五叶草", "title_jp": "ブラッククローバー", "description": "阿斯塔在没有魔力的世界中，拥有了反魔法的力量，加入黑色暴牛团，与伙伴们一起保护王国，追逐成为魔法帝的梦想。", "episodes": 170, "status": "完结", "release_year": 2017, "studio": "Studio Pierrot", "genre": "动作,冒险,奇幻", "average_rating": 8.2, "rating_count": 700000},
        {"title": "约定的梦幻岛", "title_jp": "約束のネバーランド", "description": "生活在孤儿院的孩子们发现了可怕的真相，他们是被作为食物饲养的，于是开始策划逃离，面对农场的管理者和各种危险。", "episodes": 23, "status": "完结", "release_year": 2019, "studio": "CloverWorks", "genre": "悬疑,心理,奇幻", "average_rating": 8.6, "rating_count": 600000},
        {"title": "辉夜大小姐想让我告白", "title_jp": "かぐや様は告らせたい", "description": "学生会长白银御行和副会长四宫辉夜互相喜欢，但都不愿意先告白，展开了各种智力对决和搞笑的恋爱攻防战。", "episodes": 37, "status": "完结", "release_year": 2019, "studio": "A-1 Pictures", "genre": "喜剧,恋爱,校园", "average_rating": 8.7, "rating_count": 750000},
        {"title": "JOJO的奇妙冒险", "title_jp": "ジョジョの奇妙な冒険", "description": "乔斯达家族的后代们在不同的时代展开冒险，使用替身和波纹与各种敌人战斗，讲述家族的荣耀和宿命。", "episodes": 176, "status": "连载中", "release_year": 2012, "studio": "David Production", "genre": "动作,冒险,超自然", "average_rating": 8.8, "rating_count": 900000},
        {"title": "石纪元", "title_jp": "Dr.STONE", "description": "全世界的人类都被石化，千空在数千年后苏醒，利用科学重建文明，与敌人战斗，探索石化的真相。", "episodes": 47, "status": "完结", "release_year": 2019, "studio": "TMS Entertainment", "genre": "动作,冒险,科幻", "average_rating": 8.4, "rating_count": 550000},
        {"title": "关于我转生变成史莱姆这档事", "title_jp": "転生したらスライムだった件", "description": "三上悟在异世界转生成史莱姆，拥有了独特的能力，建立了魔物之国，与各种种族交流，面对各种挑战。", "episodes": 48, "status": "连载中", "release_year": 2018, "studio": "8bit", "genre": "动作,冒险,奇幻", "average_rating": 8.3, "rating_count": 800000},
        {"title": " Re:从零开始的异世界生活", "title_jp": "Re:ゼロから始める異世界生活", "description": "菜月昴穿越到异世界，获得了死亡回归的能力，为了保护艾米莉娅和伙伴们，不断经历痛苦和死亡，寻找拯救所有人的方法。", "episodes": 50, "status": "连载中", "release_year": 2016, "studio": "White Fox", "genre": "动作,冒险,奇幻", "average_rating": 8.5, "rating_count": 950000},
        {"title": "盾之勇者成名录", "title_jp": "盾の勇者の成り上がり", "description": "岩谷尚文作为盾之勇者被召唤到异世界，遭受背叛和陷害，独自踏上冒险，与奴隶少女拉芙塔莉雅一起成长。", "episodes": 25, "status": "完结", "release_year": 2019, "studio": "Kinema Citrus", "genre": "动作,冒险,奇幻", "average_rating": 8.0, "rating_count": 700000},
        {"title": "回复术士的重启人生", "title_jp": "回復術士のやり直し", "description": "凯亚尔作为回复术士被勇者们虐待，之后他利用药物的力量回到过去，开始复仇，拯救那些曾经被勇者们伤害的人。", "episodes": 12, "status": "完结", "release_year": 2021, "studio": "TNK", "genre": "动作,冒险,奇幻", "average_rating": 7.5, "rating_count": 400000},
        {"title": "无职转生", "title_jp": "無職転生 ～異世界行ったら本気だす～", "description": "34岁的无职者转生到异世界，成为鲁迪乌斯，利用前世的知识和魔法天赋，开始新的人生，弥补前世的遗憾。", "episodes": 23, "status": "完结", "release_year": 2021, "studio": "Bind", "genre": "动作,冒险,奇幻", "average_rating": 8.2, "rating_count": 650000},
        {"title": "鬼灭之刃 无限列车篇", "title_jp": "鬼滅の刃 無限列車編", "description": "炭治郎和队友们登上无限列车，与上弦之三猗窝座战斗，炎柱炼狱杏寿郎为了保护乘客，与猗窝座展开了激烈的战斗。", "episodes": 7, "status": "完结", "release_year": 2021, "studio": "ufotable", "genre": "动作,冒险,奇幻", "average_rating": 9.4, "rating_count": 800000},
        {"title": "鬼灭之刃 游郭篇", "title_jp": "鬼滅の刃 遊郭編", "description": "炭治郎和队友们潜入吉原游郭，与上弦之六堕姬和妓夫太郎战斗，音柱宇髓天元与他们一起展开了华丽的战斗。", "episodes": 11, "status": "完结", "release_year": 2021, "studio": "ufotable", "genre": "动作,冒险,奇幻", "average_rating": 9.3, "rating_count": 750000},
        {"title": "进击的巨人 第三季", "title_jp": "進撃の巨人 Season 3", "description": "调查兵团揭开了墙壁内的真相，与王政府战斗，之后迎来了玛利亚之墙夺回战，人类终于开始了反击。", "episodes": 22, "status": "完结", "release_year": 2018, "studio": "Wit Studio", "genre": "动作,冒险,奇幻", "average_rating": 9.4, "rating_count": 900000},
        {"title": "进击的巨人 第二季", "title_jp": "進撃の巨人 Season 2", "description": "调查兵团发现了莱纳和贝尔托特的真实身份，人类面临更大的危机，开始了绝望的战斗，揭开了更多巨人的秘密。", "episodes": 12, "status": "完结", "release_year": 2017, "studio": "Wit Studio", "genre": "动作,冒险,奇幻", "average_rating": 9.3, "rating_count": 1000000},
        {"title": "火影忍者疾风传", "title_jp": "NARUTO 疾風伝", "description": "鸣人成长为强大的忍者，与晓组织战斗，拯救被抓走的我爱罗，面对佩恩的入侵，最终在第四次忍界大战中击败了辉夜。", "episodes": 500, "status": "完结", "release_year": 2007, "studio": "Studio Pierrot", "genre": "动作,冒险,奇幻", "average_rating": 8.8, "rating_count": 1600000},
    ]
    
    all_anime_data = []
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for anime in real_anime_list:
        all_anime_data.append((
            anime["title"],
            anime["title_jp"],
            anime["description"],
            f"https://picsum.photos/300/400?random={random.randint(1, 1000)}",
            anime["episodes"],
            anime["status"],
            anime["release_year"],
            anime["studio"],
            anime["genre"],
            anime["average_rating"],
            anime["rating_count"],
            created_at
        ))
    
    return all_anime_data

def main():
    print('开始生成真实动漫数据...')
    
    try:
        conn = pymysql.connect(
            host='localhost',
            database='anime_db',
            user='root',
            password='Xinmima1109'
        )
        cursor = conn.cursor()
        
        insert_query = 'INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        
        anime_data = generate_real_anime_data()
        print(f'生成了 {len(anime_data)} 条真实动漫数据')
        
        if len(anime_data) > 0:
            print('开始插入数据库...')
            cursor.executemany(insert_query, anime_data)
            conn.commit()
            print(f'成功插入 {cursor.rowcount} 条记录')
            
            cursor.execute('SELECT COUNT(*) FROM animes')
            print(f'总记录数: {cursor.fetchone()[0]}')
            
            cursor.execute('SELECT id, title, cover_image FROM animes ORDER BY id DESC LIMIT 5')
            print('\n最后5条数据:')
            for row in cursor.fetchall():
                print(row)
        else:
            print('没有生成数据')
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f'错误: {e}')

if __name__ == '__main__':
    main()
