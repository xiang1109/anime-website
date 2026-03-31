# 雾漫林间动漫网站 - 阿里云部署指南

## 快速开始

### 1. 上传项目到服务器

首先将项目文件上传到你的阿里云服务器 (59.110.214.50)

```bash
# 使用 scp 上传（本地执行）
scp -r /path/to/your/project root@59.110.214.50:/root/anime-website

# 或者使用 git 克隆（如果项目在git上）
ssh root@59.110.214.50
cd /root
git clone <your-repo-url> anime-website
```

**注意**：如果你之前已经部署过，请直接使用之前的部署目录，修改 `deploy-to-server.sh` 中的 `PROJECT_DIR` 变量。

### 2. SSH 登录到服务器

```bash
ssh root@59.110.214.50
```

### 3. 进入项目目录并设置执行权限

```bash
cd /root/anime-website  # 或者你之前的部署目录
chmod +x deploy-to-server.sh
chmod +x stop-anime-website.sh
chmod +x restart-anime-website.sh
```

### 4. 执行部署脚本

```bash
./deploy-to-server.sh
```

部署脚本会自动完成以下操作：
- 检查并安装 Node.js 和 pnpm
- 安装项目依赖
- 构建前端
- 停止旧的服务
- 启动新的后端和前端服务

### 5. 访问网站

部署完成后，访问：
- 前端: http://59.110.214.50:5000
- 后端API: http://59.110.214.50:3001

## 管理命令

### 查看服务状态

```bash
# 查看后端日志
tail -f /var/log/anime-backend.log

# 查看前端日志
tail -f /var/log/anime-frontend.log

# 查看端口占用
netstat -tlnp | grep -E ':(5000|3001)'
```

### 停止服务

```bash
./stop-anime-website.sh
```

### 重启服务

```bash
./restart-anime-website.sh
```

### 手动启动服务（如果脚本失败）

```bash
# 启动后端（后台运行）
cd /root/anime-website
nohup pnpm run server:prod > /var/log/anime-backend.log 2>&1 &

# 启动前端（后台运行）
cd /root/anime-website
nohup pnpm run preview > /var/log/anime-frontend.log 2>&1 &
```

## 管理员账号

- 用户名: `admin`
- 密码: `Xinmima1109`

## 数据库配置

数据库已经配置为线上 MySQL：
- 主机: 59.110.214.50
- 端口: 3306
- 用户: anime_user
- 密码: Xinmima1109
- 数据库: anime_db

## 兼容旧部署

如果你之前已经部署过，只需要：

1. **备份旧数据（可选）**
   ```bash
   # 备份数据库
   mysqldump -u anime_user -p anime_db > backup.sql
   ```

2. **更新项目文件**
   ```bash
   cd /path/to/your/old/deployment
   # 复制新的 dist/ 目录和 server-simple.ts 等文件
   ```

3. **修改部署脚本**
   编辑 `deploy-to-server.sh`，将 `PROJECT_DIR` 改为你旧的部署目录

4. **执行部署**
   ```bash
   ./deploy-to-server.sh
   ```

## 防火墙配置

确保阿里云安全组开放了以下端口：
- 5000 (前端)
- 3001 (后端)

在阿里云控制台配置安全组规则：
- 入方向规则：允许 TCP 5000 端口
- 入方向规则：允许 TCP 3001 端口

## 常见问题

### 1. 端口被占用

```bash
# 查看占用端口的进程
lsof -ti:5000
lsof -ti:3001

# 杀死进程
kill -9 <PID>
```

### 2. Node.js 版本过低

```bash
# 使用 nvm 安装 Node.js 20+
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
```

### 3. pnpm 未找到

```bash
npm install -g pnpm
```

### 4. 权限不足

```bash
# 确保日志目录可写
mkdir -p /var/log
chmod 755 /var/log

# 确保PID目录可写
mkdir -p /var/run
chmod 755 /var/run
```

### 5. 前端无法访问后端API

检查 `vite.config.ts` 中的代理配置是否正确：
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:3001',
    changeOrigin: true
  }
}
```

## 技术支持

如有问题，请检查：
1. 日志文件：`/var/log/anime-backend.log` 和 `/var/log/anime-frontend.log`
2. 端口占用：`netstat -tlnp`
3. 进程状态：`ps aux | grep -E 'node|tsx|vite'`
