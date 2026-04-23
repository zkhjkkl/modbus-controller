@echo off
chcp 65001 >nul
echo ========================================
echo    Modbus HTTP网关 - 二维码启动器
echo ========================================
echo.

REM 检查是否在项目目录
if not exist "gateway_launcher.py" (
    echo 错误: 请在 pc_gateway 目录运行此脚本
    pause
    exit /b 1
)

REM 检查Python
where python >nul 2>nul
if errorlevel 1 (
    echo 错误: Python未安装或未添加到PATH
    pause
    exit /b 1
)

REM 安装依赖
echo [1/3] 安装依赖...
pip install -r requirements-http.txt -q 2>nul

REM 启动网关
echo [2/3] 启动HTTP服务器...
echo.
echo   扫描二维码即可打开控制页面
echo.
echo [3/3] 打开二维码窗口...
echo.
python gateway_launcher.py

echo.
pause
