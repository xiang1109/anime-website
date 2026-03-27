import paramiko
import os
import subprocess
from datetime import datetime
import mysql.connector
from mysql.connector import Error

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

def run_local_command(command, show=True):
    if show:
        print(f"\n本地执行: {command[:100]}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if show and result.stdout:
        print(result.stdout)
    if show and result.stderr:
        print("ERR:", result.stderr)
    return result.returncode == 0, result.stdout, result.stderr

def git_commit():
    """Git提交本地代码"""
    print("\n" + "="*70)
    print("步骤 1: Git提交代码")
    print("="*70)
    
    commit_message = f"部署更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # 检查git状态
    success, out, err = run_local_command("git status")
    if not success:
        print("Git仓库未初始化，先初始化...")
        run_local_command("git init")
        run_local_command("git add .")
        run_local_command(f'git commit -m "初始化提交"')
    else:
        # 添加所有文件
        run_local_command("git add .")
        # 提交
        success, out, err = run_local_command(f'git commit -m "{commit_message}"')
        if not success and "nothing to commit" not in out + err:
            print("提交失败:", err)
        else:
            print("Git提交成功")
    
    return True

def deploy_to_server():
    """部署到服务器"""
    print("\n" + "="*70)
    print("步骤 2: 部署到服务器")
    print("="*70)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password, timeout=30)
    print("已连接到服务器")
    
    try:
        # 备份
        print("\n备份当前代码...")
        backup_dir = f"/opt/backup/anime-website-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        run_command(ssh, f"mkdir -p {backup_dir}")
        run_command(ssh, f"cp -r /opt/anime-website/* {backup_dir}/ 2>/dev/null || true")
        print(f"备份完成: {backup_dir}")
        
        # 上传数据获取脚本
        print("\n上传数据获取脚本...")
        sftp = ssh.open_sftp()
        sftp.put('fetch_anime_data.py', '/opt/anime-website/fetch_anime_data.py')
        sftp.close()
        
        # 安装Python依赖
        print("\n安装Python依赖...")
        run_command(ssh, "pip3 install requests mysql-connector-python 2>&1 | tail -5")
        
        # 安装Node.js依赖
        print("\n安装Node.js依赖...")
        run_command(ssh, "cd /opt/anime-website && npm install 2>&1 | tail -10")
        
        # 重启后端服务
        print("\n重启后端服务...")
        run_command(ssh, "pm2 restart anime-backend 2>&1")
        
        # 重启Nginx
        print("\n重启Nginx...")
        run_command(ssh, "systemctl restart nginx")
        
        # 验证服务
        print("\n验证服务状态...")
        run_command(ssh, "sleep 3")
        out, err = run_command(ssh, "curl -s http://localhost/api/health")
        print("API健康检查:", out[:100])
        
        return ssh
        
    except Exception as e:
        print(f"部署失败: {e}")
        return None

def update_anime_data(ssh):
    """更新动漫数据"""
    print("\n" + "="*70)
    print("步骤 3: 更新动漫数据")
    print("="*70)
    
    # 清空现有数据（可选）
    print("\n清空现有动漫数据...")
    run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'TRUNCATE TABLE anime_db.animes;' 2>&1")
    
    # 运行数据获取脚本
    print("\n开始获取动漫数据（这可能需要一些时间）...")
    out, err = run_command(ssh, "cd /opt/anime-website && python3 fetch_anime_data.py 2>&1", show=True)
    
    # 统计数据量
    print("\n统计数据库中的动漫数量...")
    out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) as total FROM anime_db.animes;' 2>&1")
    print("数据库中的动漫数量:", out)
    
    return True

def verify_deployment(ssh):
    """验证部署"""
    print("\n" + "="*70)
    print("步骤 4: 验证部署")
    print("="*70)
    
    # 检查服务状态
    print("\n服务状态:")
    out, err = run_command(ssh, "pm2 status anime-backend --no-color | grep anime-backend")
    print("后端:", out.strip())
    
    out, err = run_command(ssh, "systemctl is-active nginx")
    print("Nginx:", out.strip())
    
    out, err = run_command(ssh, "systemctl is-active mysqld")
    print("MySQL:", out.strip())
    
    # 测试API
    print("\nAPI测试:")
    out, err = run_command(ssh, "curl -s http://localhost/api/health")
    print("健康检查:", out[:100])
    
    out, err = run_command(ssh, "curl -s http://localhost/api/anime?page=1&limit=5")
    print("动漫数据:", out[:200])
    
    # 检查数据库记录数
    out, err = run_command(ssh, "mysql -u root -p'Xinmima1109' -e 'SELECT COUNT(*) FROM anime_db.animes;' 2>&1")
    print("\n数据库记录数:", out)
    
    ssh.close()
    
    print("\n" + "="*70)
    print("部署和数据更新完成！")
    print("="*70)
    print("\n请在浏览器中访问：")
    print("http://59.110.214.50")
    print("="*70)

def main():
    # 1. Git提交
    git_commit()
    
    # 2. 部署到服务器
    ssh = deploy_to_server()
    if not ssh:
        print("部署失败")
        return
    
    # 3. 更新动漫数据
    update_anime_data(ssh)
    
    # 4. 验证部署
    verify_deployment(ssh)

if __name__ == "__main__":
    main()
