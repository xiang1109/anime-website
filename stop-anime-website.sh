#!/bin/bash

# 停止雾漫林间动漫网站服务

echo "=========================================="
echo "停止雾漫林间动漫网站"
echo "=========================================="
echo ""

# 读取PID文件并停止进程
if [ -f "/var/run/anime-backend.pid" ]; then
    BACKEND_PID=$(cat /var/run/anime-backend.pid 2>/dev/null || true)
    if [ -n "$BACKEND_PID" ] && kill -0 $BACKEND_PID 2>/dev/null; then
        echo "停止后端服务 (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
        rm -f /var/run/anime-backend.pid
        echo "✓ 后端服务已停止"
    fi
fi

if [ -f "/var/run/anime-frontend.pid" ]; then
    FRONTEND_PID=$(cat /var/run/anime-frontend.pid 2>/dev/null || true)
    if [ -n "$FRONTEND_PID" ] && kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "停止前端服务 (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
        rm -f /var/run/anime-frontend.pid
        echo "✓ 前端服务已停止"
    fi
fi

# 额外清理可能存在的进程
pkill -f "server-simple.ts" 2>/dev/null || true
pkill -f "tsx" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

echo ""
echo "所有服务已停止"
