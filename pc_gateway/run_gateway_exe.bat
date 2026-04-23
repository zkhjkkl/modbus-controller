@echo off
echo ========================================
echo Modbus HTTP网关启动器
echo ========================================
echo.

REM 检查EXE文件是否存在
if not exist "ModbusHTTPGateway.exe" (
    echo 错误: 未找到ModbusHTTPGateway.exe
    echo 请先运行build_exe.bat打包生成EXE文件
    pause
    exit /b 1
)

echo 启动Modbus HTTP网关...
echo.
echo 请访问以下地址使用控制界面：
echo 电脑端: http://localhost:5000
echo 手机/平板: http://<电脑IP>:5000
echo.
echo 按Ctrl+C停止服务
echo ========================================
echo.

REM 运行EXE文件
ModbusHTTPGateway.exe

if errorlevel 1 (
    echo.
    echo 启动失败，请检查错误信息
    pause
)