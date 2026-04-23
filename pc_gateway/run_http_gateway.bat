@echo off
echo ========================================
echo Modbus HTTP网关启动脚本
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖...
pip install -r requirements-http.txt

echo.
echo 启动Modbus HTTP网关...
echo 请访问 http://localhost:5000
echo 平板端访问 http://<你的PC_IP>:5000
echo.

REM 运行Flask应用
python app.py

if errorlevel 1 (
    echo.
    echo 启动失败，请检查错误信息
    pause
)