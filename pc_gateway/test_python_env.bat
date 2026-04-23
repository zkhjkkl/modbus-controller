@echo off
echo 测试Python环境...
echo.

REM 测试python命令
echo 1. 测试python命令:
python --version 2>nul
if %errorlevel% equ 0 (
    echo Python已安装: python命令可用
    goto :install_deps
) else (
    echo Python命令不可用
)

echo.
echo 2. 测试py命令:
py --version 2>nul
if %errorlevel% equ 0 (
    echo Python启动器可用: py命令可用
    goto :install_deps_py
) else (
    echo py命令也不可用
)

echo.
echo 3. 检查常见Python安装位置:
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo 找到Python 3.11: C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\
    goto :use_specific_path
)

if exist "C:\Program Files\Python311\python.exe" (
    echo 找到Python 3.11: C:\Program Files\Python311\
    goto :use_specific_path
)

echo.
echo ========================================
echo 未找到Python安装！
echo 请从 python.org/downloads 下载并安装Python
echo 安装时务必勾选 "Add Python to PATH"
echo ========================================
pause
exit /b 1

:install_deps
echo.
echo 使用python安装依赖...
python -m pip install -r requirements.txt
goto :run_main

:install_deps_py
echo.
echo 使用py安装依赖...
py -m pip install -r requirements.txt
goto :run_main_py

:use_specific_path
echo.
echo 请手动运行:
echo "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" -m pip install -r requirements.txt
echo "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" main.py
pause
exit /b 0

:run_main
echo.
echo 运行主程序...
python main.py
pause
exit /b 0

:run_main_py
echo.
echo 运行主程序...
py main.py
pause
exit /b 0