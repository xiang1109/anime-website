import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Xinmima1109',
    database='anime_db',
    charset='utf8mb4'
)

cursor = conn.cursor()

print("="*70)
print("检查数据库中的动漫数据")
print("="*70)

# 查询所有动漫的ID和标题
cursor.execute("SELECT id, title, title_jp, average_rating FROM animes ORDER BY id LIMIT 10")
animes = cursor.fetchall()

print(f"\n数据库中的前10条动漫数据：")
for anime in animes:
    print(f"ID: {anime[0]}, 标题: {anime[1]}, 日文标题: {anime[2]}, 评分: {anime[3]}")

# 查询动漫总数
cursor.execute("SELECT COUNT(*) FROM animes")
total = cursor.fetchone()[0]
print(f"\n动漫总数: {total}")

conn.close()

print("\n" + "="*70)
print("检查完成")
print("="*70)
