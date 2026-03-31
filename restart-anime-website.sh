#!/bin/bash

# 重启雾漫林间动漫网站服务

echo "=========================================="
echo "重启雾漫林间动漫网站"
echo "=========================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 先停止服务
"$SCRIPT_DIR/stop-anime-website.sh"

echo ""
echo "等待2秒..."
sleep 2

# 再启动服务
"$SCRIPT_DIR/deploy-to-server.sh"
