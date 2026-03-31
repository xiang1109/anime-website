#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正动漫数据 - 修复不正确的描述和图片
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

# 热门作品的正确描述
CORRECT_DESCRIPTIONS = {
    '火影忍者': '在木叶忍者村中，鸣人从一个被孤立的孩子成长为拯救世界的英雄，讲述了友情、努力、胜利的热血故事。',
    '火影忍者疾风传': '鸣人长大成人，面对更强大的敌人，揭开晓组织的阴谋，为世界和平而战。',
    '海贼王': '草帽海贼团在伟大航路冒险，寻找传说中的One Piece，讲述了自由、友情、梦想的传奇故事。',
    '进击的巨人': '人类与巨人的生存之战，艾伦和同伴们为了自由而战，揭开世界的真相。',
    '鬼灭之刃': '炭治郎为了拯救变成鬼的妹妹，加入鬼杀队，与恶鬼展开殊死搏斗。',
    '咒术回战': '高中生虎杖悠仁吞下诅咒之王两面宿傩的手指，成为咒术师守护世界。',
    '名侦探柯南': '工藤新一被神秘组织变小，化名柯南解决各种离奇案件，寻找恢复身体的方法。',
    '银魂': '在天人来袭的江户时代，万事屋坂田银时和同伴们的搞笑日常与热血冒险。',
    '全职猎人': '小杰寻找父亲的旅程，参加猎人考试，结识伙伴，在危险世界中成长。',
    '钢之炼金术师FA': '爱德华和阿尔冯斯兄弟为了复活母亲进行人体炼成，付出惨痛代价后踏上寻找贤者之石的旅程。',
    '灌篮高手': '不良少年樱木花道为了追求赤木晴子加入篮球队，带领湘北高中征战全国大赛。',
    '网球王子': '天才少年越前龙马加入青春学园网球部，与队友们一起征战全国大赛。',
    '死神': '黑崎一护获得死神力量，守护人类灵魂，与虚和灭却师展开激烈战斗。',
    '龙珠Z': '孙悟空变身为超级赛亚人，保护地球免受宇宙强敌的威胁。',
    '刀剑神域': '桐人被困在死亡游戏中，必须通关才能离开，在游戏世界中经历冒险与爱情。',
    'Re:从零开始的异世界生活': '菜月昴穿越到异世界，获得死亡回归的能力，为了保护重要的人而不断奋斗。',
    '无职转生': '34岁无职转生到异世界，发誓要认真度过新的人生，成为强大的魔法师。',
    '关于我转生变成史莱姆这档事': '三上悟转生成史莱姆，在异世界建立魔物之国。',
    '间谍过家家': '间谍黄昏、杀手约尔、超能力者阿尼亚组成假家庭，各自隐藏身份的搞笑日常。',
    '我推的孩子': '医生转生为推的偶像的孩子，在娱乐圈复仇和成长的故事。',
    '辉夜大小姐想让我告白': '学生会会长白银御行和副会长四宫辉夜互相暗恋，都想让对方先告白的恋爱喜剧。',
    '灵能百分百': '龙套拥有超强超能力，但只想过普通生活，在灵幻新隆的指导下成长。',
    '我的青春恋爱物语果然有问题': '比企谷八幡在侍奉部与雪之下雪乃、由比滨结衣一起解决各种校园问题。',
    '葬送的芙莉莲': '勇者队伍的魔法师芙莉莲在勇者死后，与新伙伴一起旅行，理解人类的感情。',
    '迷宫饭': '冒险者莱欧斯在迷宫中一边寻找妹妹，一边用魔物制作美食的冒险故事。',
    '药屋少女的呢喃': '被卖到后宫的药师猫猫，用医学知识解决各种谜题。',
    '国王排名': '波吉王子虽然又聋又哑，但仍想成为最棒的国王，与卡克一起踏上冒险。',
    '来自深渊': '莉可和雷格前往深渊深处寻找母亲，揭开深渊的神秘面纱。',
    '强风吹拂': '清濑灰二带领竹青庄的房客们参加箱根驿传，讲述跑步的意义。',
    '四叠半神话大系': '大学生在四叠半宿舍中不断轮回，寻找理想的大学生活。',
    '乒乓': '星野裕和月本诚两个天才乒乓球手的竞争与友情。',
    '昭和元禄落语心中': '与太郎在监狱中遇到落语家八云，拜师学艺，传承落语艺术。',
    '比宇宙更远的地方': '四位女高中生一起去南极的青春冒险故事。',
    '三月的狮子': '将棋天才桐山零在经历家庭变故后，与川本三姐妹相遇，逐渐走出孤独。',
    '紫罗兰永恒花园': '战争结束后，薇尔莉特成为自动手记人偶，寻找「我爱你」的含义。',
    'CLANNAD': '冈崎朋也在高中遇到古河渚，一起经历青春、家庭、人生的温暖故事。',
    '冰菓': '节能主义者折木奉太郎在古典部与千反田爱瑠一起解开各种谜题。',
    '吹响！悠风号': '黄前久美子加入北宇治高中吹奏部，以全国大赛为目标而奋斗。',
    '孤独摇滚！': '社恐少女后藤一里为了交到朋友而组建乐队，在音乐中成长。',
    '摇曳露营△': '各务原抚子与志摩凛一起露营，享受户外生活的治愈故事。',
    '别对映像研出手！': '浅草绿、金森沙耶香、水崎燕三位少女一起制作动画的故事。',
    '大欺诈师': '枝村真人被卷入国际诈骗，与罗兰一起在世界各地进行诈骗冒险。',
    '黄金神威': '杉元佐一和阿席莉帕在北海道寻找黄金，与各种敌人战斗。',
    '佐贺偶像是传奇': "七位少女僵尸组成偶像团体，复兴佐贺的搞笑故事。",
    '灵笼': '人类在末世中生活在浮空堡垒灯塔上，与地面的噬极兽战斗。',
    '三体': '叶文洁向宇宙发出信号，引来三体文明，人类面临前所未有的危机。',
    '中国奇谭': '八个中国风格的奇幻故事，展现传统文化的魅力。',
    '雾山五行': '闻人翊悬在雾山中与妖兽战斗，守护五行平衡。',
    '大理寺日志': '李饼在大理寺为官，与陈拾一起解决各种案件。',
    '时光代理人': '程小时和陆光通过照片回到过去，完成客户的委托。',
    '天官赐福': '仙乐太子谢怜第三次飞升，与鬼界花城相遇，揭开三界的秘密。',
    '完美世界': '石昊在大荒中成长，从石村走向更广阔的世界，成为荒天帝。',
    '斗破苍穹': '萧炎从天才沦为废柴，在药老的帮助下重新崛起，成为炎帝。',
    '一念永恒': '白小纯追求长生不老，在修仙界闹出各种笑话，最终成为永恒。',
    '凡人修仙传': '韩立从平凡少年开始，一步步修仙，历经无数艰险。',
    '狐妖小红娘': '涂山苏苏和白月初一起帮助妖怪们完成转世续缘。',
    '一人之下': '张楚岚在异人世界中寻找爷爷的真相，与冯宝宝一起冒险。',
    '全职高手': '叶修被战队开除后，在荣耀网游中重新回到巅峰。',
    '刺客伍六七': '伍六七在小鸡岛上做刺客，其实是为了找回失去的记忆。',
    '罗小黑战记': '猫妖罗小黑在人类世界中冒险，与小白成为朋友。'
}

# 更好的封面图片服务
def get_better_cover(anime_id, title):
    """生成更好的封面图片"""
    # 使用多个不同的图片服务
    services = [
        f"https://picsum.photos/seed/anime{anime_id}/300/400",
        f"https://placehold.co/300x400/e8e8e8/333?text={title[:10]}",
    ]
    return random.choice(services)

def main():
    """主函数"""
    print("=" * 70)
    print("修正动漫数据 - 修复不正确的描述和图片")
    print("=" * 70)
    print()
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
        print()
        
        cursor = connection.cursor(dictionary=True)
        
        # 1. 更新热门作品的描述
        print("正在更新热门作品的描述...")
        update_count = 0
        
        for title, desc in CORRECT_DESCRIPTIONS.items():
            # 查找所有包含这个标题的作品
            cursor.execute("""
                SELECT id, title, description 
                FROM animes 
                WHERE title LIKE %s
            """, (f"%{title}%",))
            
            matches = cursor.fetchall()
            
            for anime in matches:
                # 更新描述
                cursor.execute("""
                    UPDATE animes 
                    SET description = %s,
                        cover_image = %s
                    WHERE id = %s
                """, (desc, get_better_cover(anime['id'], anime['title']), anime['id']))
                
                update_count += 1
                print(f"  ✓ 更新: {anime['title']}")
        
        connection.commit()
        print(f"✓ 更新了 {update_count} 条热门作品数据")
        print()
        
        # 2. 修正一些明显错误的描述
        print("正在修正其他明显错误的描述...")
        fix_count = 0
        
        # 查找包含"爱情故事"但应该是战斗的作品
        battle_keywords = ['火影', '忍者', '海贼', '进击', '巨人', '鬼灭', '咒术', '死神', '龙珠', '战斗', '冒险']
        
        for keyword in battle_keywords:
            cursor.execute("""
                SELECT id, title, description 
                FROM animes 
                WHERE title LIKE %s 
                AND description LIKE '%爱情%'
            """, (f"%{keyword}%",))
            
            matches = cursor.fetchall()
            
            for anime in matches:
                # 根据标题类型生成合适的描述
                if '火影' in anime['title'] or '忍者' in anime['title']:
                    new_desc = '在忍者世界中，忍者们为了守护村子和同伴，进行着激烈的战斗与成长。'
                elif '海贼' in anime['title']:
                    new_desc = '在广阔的大海上，海贼们为了梦想和财宝，展开了惊心动魄的冒险。'
                elif '进击' in anime['title'] or '巨人' in anime['title']:
                    new_desc = '人类在高墙之中躲避巨人，为了自由和生存，与巨人展开殊死搏斗。'
                elif '鬼灭' in anime['title']:
                    new_desc = '鬼杀队的剑士们为了保护人类，与恶鬼展开激烈的战斗，守护家人与朋友。'
                elif '咒术' in anime['title']:
                    new_desc = '咒术师们使用咒力对抗诅咒，守护人类社会免受诅咒的侵害。'
                elif '死神' in anime['title']:
                    new_desc = '死神们守护着灵魂的世界，与虚和其他邪恶势力战斗，维护生死平衡。'
                elif '龙珠' in anime['title']:
                    new_desc = '战士们为了保护地球，不断修炼变强，与来自宇宙的强敌战斗。'
                else:
                    new_desc = '在这个充满冒险的世界中，主角与伙伴们一起经历各种挑战，不断成长变强。'
                
                cursor.execute("""
                    UPDATE animes 
                    SET description = %s,
                        cover_image = %s
                    WHERE id = %s
                """, (new_desc, get_better_cover(anime['id'], anime['title']), anime['id']))
                
                fix_count += 1
                print(f"  ✓ 修正: {anime['title']}")
        
        connection.commit()
        print(f"✓ 修正了 {fix_count} 条错误描述")
        print()
        
        # 3. 更新更多的封面图片，让它们更有意义
        print("正在优化更多封面图片...")
        cursor.execute("""
            SELECT id, title 
            FROM animes 
            ORDER BY RAND() 
            LIMIT 500
        """)
        random_animes = cursor.fetchall()
        
        image_count = 0
        for anime in random_animes:
            cursor.execute("""
                UPDATE animes 
                SET cover_image = %s
                WHERE id = %s
            """, (get_better_cover(anime['id'], anime['title']), anime['id']))
            image_count += 1
        
        connection.commit()
        print(f"✓ 优化了 {image_count} 张封面图片")
        print()
        
        # 统计
        print("=" * 70)
        print("数据修正完成！")
        print(f"- 更新热门作品描述: {update_count} 条")
        print(f"- 修正错误描述: {fix_count} 条")
        print(f"- 优化封面图片: {image_count} 张")
        print(f"- 总计修正: {update_count + fix_count + image_count} 条")
        print("=" * 70)
        
        # 展示一些修正后的例子
        print()
        print("📌 修正后的作品示例:")
        cursor.execute("""
            SELECT id, title, description, cover_image
            FROM animes 
            ORDER BY id DESC 
            LIMIT 10
        """)
        examples = cursor.fetchall()
        
        for i, anime in enumerate(examples, 1):
            print(f"\n{i}. {anime['title']}")
            print(f"   描述: {anime['description'][:50]}...")
        
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
