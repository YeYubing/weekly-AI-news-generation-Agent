#!/bin/bash

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装必要依赖
echo "检查依赖..."
pip3 install --upgrade pip

# 运行主程序
echo "启动AI播报助手..."
python3 ai_reporter.py

# 保持窗口打开
echo ""
echo "按回车键退出..."
read -p ""

