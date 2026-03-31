#!/bin/bash

echo "🎬 动漫图片管理系统启动脚本"
echo "=================================="
echo ""

# 检查是否安装了依赖
if [ ! -d "node_modules" ]; then
    echo "📦 正在安装依赖..."
    pnpm install
fi

# 复制环境变量文件
if [ ! -f ".env" ]; then
    echo "⚙️  正在创建环境变量文件..."
    cp .env.example .env
fi

echo ""
echo "✅ 准备完成！"
echo ""
echo "请按以下步骤启动："
echo ""
echo "1. 启动后端服务器（新终端窗口）："
echo "   pnpm run server"
echo ""
echo "2. 启动前端开发服务器（新终端窗口）："
echo "   pnpm run dev"
echo ""
echo "3. 访问管理页面："
echo "   前端地址: http://localhost:5000"
echo "   管理路径: /anime-manager"
echo ""
echo "📖 详细说明请查看 ANIME_MANAGER_GUIDE.md"
echo ""
