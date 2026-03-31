#!/bin/bash

# 雾漫林间动漫网站部署脚本
# 阿里云服务器: 59.110.214.50

set -e

echo "=========================================="
echo "雾漫林间动漫网站部署脚本"
echo "=========================================="
echo ""

# 配置变量
PROJECT_DIR="/root/anime-website"  # 或者你之前的部署目录
BACKEND_PORT=3001
FRONTEND_PORT=5000

echo "1. 检查项目目录..."
if [ ! -d "$PROJECT_DIR" ]; then
    echo "   目录不存在，请先上传项目文件到 $PROJECT_DIR"
    echo "   或者修改脚本中的 PROJECT_DIR 为你之前的部署目录"
    exit 1
fi

cd "$PROJECT_DIR"
echo "   ✓ 进入项目目录: $PWD"
echo ""

echo "2. 检查Node.js和pnpm..."
if ! command -v node &> /dev/null; then
    echo "   ✗ Node.js 未安装，请先安装 Node.js 20+"
    exit 1
fi
echo "   ✓ Node.js 版本: $(node --version)"

if ! command -v pnpm &> /dev/null; then
    echo "   安装 pnpm..."
    npm install -g pnpm
fi
echo "   ✓ pnpm 版本: $(pnpm --version)"
echo ""

echo "3. 安装依赖..."
pnpm install
echo "   ✓ 依赖安装完成"
echo ""

echo "4. 构建前端..."
pnpm run build
echo "   ✓ 前端构建完成"
echo ""

echo "5. 检查并停止旧进程..."
# 停止旧的后端进程
if lsof -ti:$BACKEND_PORT > /dev/null; then
    echo "   停止旧的后端服务 (端口 $BACKEND_PORT)..."
    pkill -f "server-simple.ts" || true
    pkill -f "tsx" || true
    sleep 2
fi

# 停止旧的前端进程
if lsof -ti:$FRONTEND_PORT > /dev/null; then
    echo "   停止旧的前端服务 (端口 $FRONTEND_PORT)..."
    pkill -f "vite" || true
    sleep 2
fi
echo "   ✓ 旧进程清理完成"
echo ""

echo "6. 启动后端服务..."
cd "$PROJECT_DIR"
nohup pnpm run server:prod > /var/log/anime-backend.log 2>&1 &
BACKEND_PID=$!
echo "   ✓ 后端服务已启动 (PID: $BACKEND_PID)"
echo "   日志: /var/log/anime-backend.log"
echo ""

echo "7. 等待后端服务启动..."
sleep 5

# 检查后端是否启动成功
if curl -s "http://localhost:$BACKEND_PORT/api/health" > /dev/null; then
    echo "   ✓ 后端服务启动成功"
else
    echo "   ✗ 后端服务启动失败，请检查日志"
    echo "   tail -f /var/log/anime-backend.log"
fi
echo ""

echo "8. 启动前端服务..."
cd "$PROJECT_DIR"
nohup pnpm run preview > /var/log/anime-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   ✓ 前端服务已启动 (PID: $FRONTEND_PID)"
echo "   日志: /var/log/anime-frontend.log"
echo ""

echo "9. 保存进程ID..."
echo "$BACKEND_PID" > /var/run/anime-backend.pid
echo "$FRONTEND_PID" > /var/run/anime-frontend.pid
echo ""

echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo ""
echo "访问地址："
echo "  前端: http://59.110.214.50:$FRONTEND_PORT"
echo "  后端: http://59.110.214.50:$BACKEND_PORT"
echo ""
echo "管理命令："
echo "  查看后端日志: tail -f /var/log/anime-backend.log"
echo "  查看前端日志: tail -f /var/log/anime-frontend.log"
echo "  停止服务: ./stop-anime-website.sh"
echo "  重启服务: ./restart-anime-website.sh"
echo ""
echo "管理员账号："
echo "  用户名: admin"
echo "  密码: Xinmima1109"
echo ""
