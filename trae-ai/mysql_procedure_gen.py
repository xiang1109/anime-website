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
print("使用MySQL存储过程生成5000条数据")
print("="*70)

# 1. 创建存储过程
print("\n=== 1. 创建存储过程 ===")

procedure_sql = """
USE anime_db;

DELIMITER $$

DROP PROCEDURE IF EXISTS insert_anime_data$$

CREATE PROCEDURE insert_anime_data()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE max_i INT DEFAULT 5000;
    
    WHILE i <= max_i DO
        INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at)
        VALUES (
            CONCAT('动漫 ', FLOOR(1 + (RAND() * 100)), ' 第', FLOOR(1 + (RAND() * 10)), '季'),
            CONCAT('アニメ', FLOOR(1 + (RAND() * 100))),
            '这是关于冒险、友情和成长的故事，讲述了主角们的精彩旅程。',
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
        );
        
        SET i = i + 1;
        
        IF i % 100 = 0 THEN
            SELECT CONCAT('已插入 ', i, ' 条记录') AS progress;
            COMMIT;
        END IF;
    END WHILE;
    
    COMMIT;
    SELECT CONCAT('总共插入 ', max_i, ' 条记录') AS result;
END$$

DELIMITER ;
"""

run_command(ssh, f"mysql -u root -p'Xinmima1109' <<'EOF'\n{procedure_sql}\nEOF")
print("存储过程已创建")

# 2. 清空表
print("\n=== 2. 清空表 ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'TRUNCATE TABLE anime_db.animes;' 2>&1")

# 3. 执行存储过程
print("\n=== 3. 执行存储过程（这可能需要几分钟） ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'USE anime_db; CALL insert_anime_data();' 2>&1")
print(out)

# 4. 检查数据量
print("\n=== 4. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 5. 检查数据示例
print("\n=== 5. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating, cover_image FROM anime_db.animes ORDER BY id DESC LIMIT 3;' 2>&1")
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
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=10&limit=10'")
print(out[:300])

ssh.close()

print("\n" + "="*70)
print("数据生成完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在数据库中有5000条动漫数据！")
print("="*70)
