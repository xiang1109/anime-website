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
print("在服务器上更新动漫图片")
print("="*70)

# 创建更新图片的SQL脚本
sql_script = '''
-- 更新动漫图片
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/10/47347.jpg' WHERE title = '进击的巨人';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/6/73245.jpg' WHERE title = '海贼王';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/13/17405.jpg' WHERE title = '火影忍者';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/1286/108766.jpg' WHERE title = '鬼灭之刃';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/1171/109282.jpg' WHERE title = '咒术回战';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/5/73147.jpg' WHERE title = '东京食尸鬼';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/10/78745.jpg' WHERE title = '我的英雄学院';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/11/39717.jpg' WHERE title = '刀剑神域';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/7/20951.jpg' WHERE title = '名侦探柯南';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/9/21427.jpg' WHERE title = '死亡笔记';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/1223/96541.jpg' WHERE title = '钢之炼金术师';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/1908/110531.jpg' WHERE title = '进击的巨人 最终季';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/1796/111223.jpg' WHERE title = '鬼灭之刃 无限列车篇';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/1314/93463.jpg' WHERE title = '进击的巨人 第三季';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/5/64785.jpg' WHERE title = '排球少年';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/11/55501.jpg' WHERE title = '全职猎人';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/4/73935.jpg' WHERE title = '夏目友人帐';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/10/7370.jpg' WHERE title = '银魂';
UPDATE animes SET cover_image = 'https://cdn.myanimelist.net/images/anime/4/73244.jpg' WHERE title = '黑执事';
'''

# 上传SQL脚本
sftp = ssh.open_sftp()
from io import BytesIO
sql_file = BytesIO(sql_script.encode('utf-8'))
sftp.putfo(sql_file, '/root/update_anime_images.sql')
sftp.close()

# 执行SQL脚本
print("\n执行SQL脚本更新图片...")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' anime_db < /root/update_anime_images.sql 2>&1")
print(out)
if err:
    print("错误:", err)

# 验证更新结果
print("\n验证更新结果...")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, cover_image FROM anime_db.animes ORDER BY id LIMIT 10;' 2>&1")
print(out)

ssh.close()

print("\n" + "="*70)
print("动漫图片更新完成！")
print("="*70)
print("\n请刷新浏览器查看更新后的动漫图片！")
print("="*70)
