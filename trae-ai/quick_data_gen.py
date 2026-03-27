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
print("快速生成5000条动漫数据")
print("="*70)

# 1. 清空表
print("\n=== 1. 清空表 ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'TRUNCATE TABLE anime_db.animes;' 2>&1")

# 2. 创建SQL脚本
print("\n=== 2. 创建SQL脚本 ===")

# 直接在服务器上创建SQL生成脚本
sql_gen_script = """
USE anime_db;

DELIMITER $$

DROP PROCEDURE IF EXISTS generate_anime_data$$

CREATE PROCEDURE generate_anime_data()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE batch_size INT DEFAULT 100;
    DECLARE total INT DEFAULT 5000;
    
    WHILE i <= total DO
        INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at)
        SELECT 
            CONCAT('动漫 ', FLOOR(1 + (RAND() * 100)), ' 第', FLOOR(1 + (RAND() * 10)), '季'),
            CONCAT('アニメ', FLOOR(1 + (RAND() * 100))),
            CONCAT('这是关于冒险、友情和成长的故事，讲述了主角们的精彩旅程。'),
            CONCAT('https://picsum.photos/300/400?random=', i),
            FLOOR(12 + (RAND() * 100)),
            CASE WHEN RAND() > 0.5 THEN '完结' ELSE '连载中' END,
            FLOOR(1990 + (RAND() * 35)),
            CASE FLOOR(1 + (RAND() * 5))
                WHEN 1 THEN 'Madhouse'
                WHEN 2 THEN 'ufotable'
                WHEN 3 THEN 'Bones'
                WHEN 4 THEN 'MAPPA'
                ELSE '东映动画'
            END,
            CASE FLOOR(1 + (RAND() * 5))
                WHEN 1 THEN '动作,冒险,奇幻'
                WHEN 2 THEN '悬疑,犯罪,剧情'
                WHEN 3 THEN '爱情,剧情'
                WHEN 4 THEN '科幻,悬疑'
                ELSE '喜剧,动作'
            END,
            ROUND(7.0 + (RAND() * 2.8), 2),
            FLOOR(1000 + (RAND() * 49000)),
            NOW()
        FROM information_schema.tables t1, information_schema.tables t2
        LIMIT batch_size;
        
        SET i = i + batch_size;
        SELECT CONCAT('已插入 ', i, ' 条记录') AS progress;
    END WHILE;
    
    SELECT CONCAT('总共插入 ', total, ' 条记录') AS result;
END$$

DELIMITER ;

CALL generate_anime_data();
"""

run_command(ssh, f"cat > /tmp/generate_anime.sql <<'EOF'\n{sql_gen_script}\nEOF")
print("SQL脚本已创建")

# 3. 执行SQL脚本
print("\n=== 3. 执行SQL脚本 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' < /tmp/generate_anime.sql 2>&1", show=True)
print("SQL执行完成")

# 4. 检查数据量
print("\n=== 4. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 5. 检查数据示例
print("\n=== 5. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating, cover_image FROM anime_db.animes LIMIT 5;' 2>&1")
print(out)

# 6. 测试API
print("\n=== 6. 测试API ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=5'")
print(out[:500])

# 7. 重启后端服务
print("\n=== 7. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend 2>&1")
run_command(ssh, "sleep 2")

# 8. 测试分页
print("\n=== 8. 测试分页 ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=2&limit=10'")
print(out[:300])

ssh.close()

print("\n" + "="*70)
print("数据生成完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在数据库中有5000条动漫数据！")
print("="*70)
