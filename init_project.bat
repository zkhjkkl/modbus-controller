@echo off
echo ========================================
echo    Flutter项目初始化脚本
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
echo [1/4] 检查Flutter环境...
flutter --version
echo.

REM 进入项目目录
cd tablet_app

REM 检查是否已有平台文件
if exist "android\app\src\main\AndroidManifest.xml" (
    echo [2/4] Android项目文件已存在
    echo 跳过平台文件生成...
) else (
    echo [2/4] 生成Android平台文件...
    flutter create --platforms=android .
    if errorlevel 1 (
        echo 错误: 生成平台文件失败
        pause
        exit /b 1
    )
    echo Android项目文件已生成
)

REM 检查iOS平台文件（可选）
if exist "ios\Runner\Info.plist" (
    echo [3/4] iOS项目文件已存在
) else (
    echo [3/4] 如需iOS支持，请运行: flutter create --platforms=ios .
)

REM 获取依赖
echo [4/4] 安装项目依赖...
flutter pub get
if errorlevel 1 (
    echo 错误: 安装依赖失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 项目初始化完成！
echo.
echo 项目结构:
echo   android/          - Android项目文件
echo   ios/              - iOS项目文件（如需）
echo   lib/main.dart     - 主程序代码
echo   pubspec.yaml      - 依赖配置
echo.
echo 下一步:
echo 1. 运行 build_apk.bat 构建APK
echo 2. 或运行 flutter run 直接测试
echo ========================================
echo.

REM 返回原目录
cd ..

pause