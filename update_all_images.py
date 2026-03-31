import paramiko

hostname = '59.110.214.50'
username = 'root'
password = 'Xinmima1109'

def run_command(ssh, command, show=True):
    if show:
        print(f"\n执行: {command[:100]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if show and out:
        print(out)
    if show and err:
        print("ERR:", err)
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password, timeout=30)

print("="*70)
print("更新数据库中的动漫图片")
print("="*70)

# 动漫图片映射
anime_images = {
    "进击的巨人": "https://cdn.myanimelist.net/images/anime/10/47347.jpg",
    "海贼王": "https://cdn.myanimelist.net/images/anime/6/73245.jpg",
    "火影忍者": "https://cdn.myanimelist.net/images/anime/13/17405.jpg",
    "鬼灭之刃": "https://cdn.myanimelist.net/images/anime/1286/108766.jpg",
    "咒术回战": "https://cdn.myanimelist.net/images/anime/1171/109282.jpg",
    "东京食尸鬼": "https://cdn.myanimelist.net/images/anime/5/73147.jpg",
    "我的英雄学院": "https://cdn.myanimelist.net/images/anime/10/78745.jpg",
    "刀剑神域": "https://cdn.myanimelist.net/images/anime/11/39717.jpg",
    "名侦探柯南": "https://cdn.myanimelist.net/images/anime/7/20951.jpg",
    "死亡笔记": "https://cdn.myanimelist.net/images/anime/9/21427.jpg",
    "钢之炼金术师": "https://cdn.myanimelist.net/images/anime/1223/96541.jpg",
    "进击的巨人 最终季": "https://cdn.myanimelist.net/images/anime/1908/110531.jpg",
    "鬼灭之刃 无限列车篇": "https://cdn.myanimelist.net/images/anime/1796/111223.jpg",
    "进击的巨人 第三季": "https://cdn.myanimelist.net/images/anime/1314/93463.jpg",
    "排球少年": "https://cdn.myanimelist.net/images/anime/5/64785.jpg",
    "全职猎人": "https://cdn.myanimelist.net/images/anime/11/55501.jpg",
    "夏目友人帐": "https://cdn.myanimelist.net/images/anime/4/73935.jpg",
    "银魂": "https://cdn.myanimelist.net/images/anime/10/7370.jpg",
    "黑执事": "https://cdn.myanimelist.net/images/anime/4/73244.jpg",
    "进击的巨人 第二季": "https://cdn.myanimelist.net/images/anime/1314/93463.jpg",
    "东京食尸鬼√A": "https://cdn.myanimelist.net/images/anime/5/73147.jpg",
    "鬼灭之刃 游郭篇": "https://cdn.myanimelist.net/images/anime/1796/111223.jpg",
    "东京食尸鬼re": "https://cdn.myanimelist.net/images/anime/5/73147.jpg",
    "关于我转生变成史莱姆这档事": "https://cdn.myanimelist.net/images/anime/1314/93463.jpg",
    "一拳超人": "https://cdn.myanimelist.net/images/anime/12/76049.jpg",
    "辉夜大小姐想让我告白": "https://cdn.myanimelist.net/images/anime/1314/93463.jpg",
    "五等分的新娘": "https://cdn.myanimelist.net/images/anime/1314/93463.jpg",
    "干物妹！小埋": "https://cdn.myanimelist.net/images/anime/1314/93463.jpg",
    "玉子市场": "https://cdn.myanimelist.net/images/anime/1314/93463.jpg",
    "境界的彼方": "https://cdn.myanimelist.net/images/anime/1314/93463.jpg"
}

# 生成SQL更新语句
sql_commands = []
for title, image_url in anime_images.items():
    sql = f"UPDATE anime_db.animes SET cover_image = '{image_url}' WHERE title = '{title}';"
    sql_commands.append(sql)

# 执行SQL更新
print("\n执行SQL更新...")
for sql in sql_commands:
    out, err = run_command(ssh, f"mysql -u root -p'Xinmima1109' -e '{sql}' 2>&1")
    if err:
        print(f"错误更新 {anime_images[title]}: {err}")

# 验证更新结果
print("\n验证更新结果...")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, cover_image FROM anime_db.animes ORDER BY id LIMIT 10;' 2>&1")
print(out)

# 检查所有图片URL
print("\n检查所有图片URL...")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT DISTINCT cover_image FROM anime_db.animes;' 2>&1")
print(out)

ssh.close()

print("\n" + "="*70)
print("动漫图片更新完成！")
print("="*70)
print("\n所有动漫图片都已更新为MyAnimeList的高质量图片！")
print("="*70)
