@echo off
echo ========================================
echo    Modbus控制器APK构建脚本
echo ========================================
echo.

REM 检查是否在项目根目录
if not exist "tablet_app\pubspec.yaml" (
    echo 错误: 请在项目根目录运行此脚本
    echo 当前目录: %cd%
    echo 找不到 tablet_app\pubspec.yaml
    pause
    exit /b 1
)

REM 检查Flutter是否安装
where flutter >nul 2>nul
if errorlevel 1 (
    echo 错误: Flutter未安装或未添加到PATH
    echo 请先安装Flutter SDK并配置环境变量
    echo 参考 BUILD_GUIDE.md 文档
    pause
    exit /b 1
)

REM 显示Flutter版本
echo [1/6] 检查Flutter环境...
flutter --version
echo.

REM 检查Android环境
echo [2/6] 检查Android开发环境...
flutter doctor --android-licenses
echo.

REM 进入项目目录
cd tablet_app

REM 清理项目
echo [3/6] 清理项目...
flutter clean
if errorlevel 1 (
    echo 错误: 清理项目失败
    pause
    exit /b 1
)
echo.

REM 获取依赖
echo [4/6] 安装依赖...
flutter pub get
if errorlevel 1 (
    echo 错误: 获取依赖失败
    pause
    exit /b 1
)
echo.

REM 构建APK
echo [5/6] 构建APK（发布版）...
echo 这可能需要几分钟，请耐心等待...
flutter build apk --release
if errorlevel 1 (
    echo 错误: 构建APK失败
    pause
    exit /b 1
)
echo.

REM 显示APK位置
echo [6/6] 构建完成！
echo.
echo ========================================
echo APK文件位置:
echo.
echo 发布版APK:
echo   tablet_app\build\app\outputs\apk\release\app-release.apk
echo.
echo 调试版APK（如需）:
echo   flutter build apk --debug
echo.
echo ========================================
echo 安装到设备:
echo 1. 通过USB: adb install app-release.apk
echo 2. 复制到设备手动安装
echo.
echo 测试应用:
echo 1. 确保PC端网关正在运行
echo 2. 配置服务器地址为 PC_IP:8765
echo 3. 点击"连接"按钮
echo ========================================
echo.

REM 返回原目录
cd ..

pause