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
print("使用MySQL命令行生成5000条数据")
print("="*70)

# 1. 清空表
print("\n=== 1. 清空表 ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'TRUNCATE TABLE anime_db.animes;' 2>&1")

# 2. 创建一个简单的SQL脚本，使用存储过程
print("\n=== 2. 创建存储过程 ===")

# 先创建一个简单的SQL文件
sql_script = """
USE anime_db;

DELIMITER $$

DROP PROCEDURE IF EXISTS insert_5000_animes$$

CREATE PROCEDURE insert_5000_animes()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 5000 DO
        INSERT INTO animes (title, title_jp, description, cover_image, episodes, status, release_year, studio, genre, average_rating, rating_count, created_at)
        VALUES (
            CONCAT('动漫 ', i),
            CONCAT('アニメ', i),
            '这是关于冒险、友情和成长的故事',
            CONCAT('https://picsum.photos/300/400?random=', i),
            24,
            '连载中',
            2020,
            'Studio',
            '动作,冒险',
            8.5,
            1000,
            NOW()
        );
        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;
"""

# 写入SQL文件
sftp = ssh.open_sftp()
with sftp.file('/tmp/insert_5000_animes.sql', 'w') as f:
    f.write(sql_script)
sftp.close()
print("SQL文件已写入")

# 3. 执行存储过程
print("\n=== 3. 执行存储过程（这可能需要几分钟） ===")
run_command(ssh, "mysql -u root -p'Xinmima1109' < /tmp/insert_5000_animes.sql 2>&1")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'USE anime_db; CALL insert_5000_animes();' 2>&1")
print("存储过程执行完成")

# 4. 检查数据量
print("\n=== 4. 检查数据量 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
print(out)

# 5. 检查数据示例
print("\n=== 5. 检查数据示例 ===")
out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT id, title, average_rating FROM anime_db.animes ORDER BY id DESC LIMIT 5;' 2>&1")
print(out)

# 6. 测试API
print("\n=== 6. 测试API ===")
out, err = run_command(ssh, "curl -s 'http://localhost/api/anime?page=1&limit=5'")
print(out[:500])

# 7. 重启后端服务
print("\n=== 7. 重启后端服务 ===")
run_command(ssh, "pm2 restart anime-backend 2>&1")
run_command(ssh, "sleep 2")

ssh.close()

print("\n" + "="*70)
print("数据生成完成！")
print("="*70)
print("\n请在浏览器中访问：")
print("http://59.110.214.50")
print("\n现在数据库中有5000条动漫数据！")
print("="*70)
