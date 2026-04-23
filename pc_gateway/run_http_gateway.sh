#!/bin/bash

echo "========================================"
echo "Modbus HTTP网关启动脚本"
echo "========================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.6+"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
pip3 install -r requirements-http.txt

echo ""
echo "启动Modbus HTTP网关..."
echo "请访问 http://localhost:5000"
echo "平板端访问 http://<你的PC_IP>:5000"
echo ""

# 运行Flask应用
python3 app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "启动失败，请检查错误信息"
    exit 1
fi