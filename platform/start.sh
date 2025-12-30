#!/bin/bash
# 人工标注核验平台启动脚本

echo "🚀 启动人工标注核验平台..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
pip install -r requirements.txt

# 创建必要目录
mkdir -p annotated_data

# 启动Flask应用
echo "🌐 启动Web服务..."
echo "📍 访问地址: http://localhost:5000"
echo "⏹️  按 Ctrl+C 停止服务"
echo ""

python app.py
