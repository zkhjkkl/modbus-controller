@echo off
chcp 65001 >nul
echo ========================================
echo    二维码Modbus网关 - EXE构建脚本
echo ========================================
echo.
echo 将打包成一个EXE文件，双击即可运行（无终端窗口）
echo.

REM 检查Python
where python >nul 2>nul
if errorlevel 1 (
    echo 错误: Python未安装或未添加到PATH
    pause
    exit /b 1
)

REM 安装PyInstaller
echo [1/4] 检查PyInstaller...
pip show PyInstaller >nul 2>nul
if errorlevel 1 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
)

REM 安装依赖
echo [2/4] 安装依赖...
pip install -r requirements-http.txt

REM 清理旧的构建文件
echo [3/4] 清理旧的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "ModbusGateway.spec" del /q ModbusGateway.spec

REM 构建EXE（--noconsole 隐藏终端窗口）
echo [4/4] 正在构建EXE文件（可能需要几分钟）...
echo.

pyinstaller --onefile --noconsole ^
    --name "ModbusGateway" ^
    --add-data "templates;templates" ^
    --add-data "config.json;." ^
    --hidden-import qrcode ^
    --hidden-import PIL ^
    --hidden-import PIL._tkinter_finder ^
    --collect-all qrcode ^
    --collect-all PIL ^
    --clean ^
    gateway_launcher.py

if errorlevel 1 (
    echo.
    echo 构建失败！请检查上方错误信息。
    pause
    exit /b 1
)

echo.
echo ========================================
echo 构建成功！
echo ========================================
echo EXE文件: dist\ModbusGateway.exe
echo.
echo 使用说明：
echo 1. 双击 ModbusGateway.exe（无终端窗口）
echo 2. 弹出二维码窗口
echo 3. 手机扫描二维码即可打开控制页面
echo 4. 关闭二维码窗口即可停止服务器
echo.
echo 注意：首次运行可能需要防火墙授权
echo ========================================
echo.
pause
