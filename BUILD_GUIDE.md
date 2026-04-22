# Flutter APK 构建指南

本指南详细说明如何在Windows系统上构建Android APK。

## 系统要求
- Windows 10/11 64位
- 至少8GB RAM
- 至少10GB可用磁盘空间
- 稳定的网络连接

## 第1步：安装Flutter SDK

### 1.1 下载Flutter SDK
1. 访问 [Flutter官网](https://flutter.dev/docs/get-started/install/windows)
2. 下载 **Flutter SDK**（稳定版）
3. 解压到合适位置，例如：`C:\src\flutter`
   - **不要**解压到`C:\Program Files\`（权限问题）
   - **不要**解压到有中文或空格的路径

### 1.2 配置环境变量
1. 右键点击"此电脑" → "属性" → "高级系统设置" → "环境变量"
2. 在"用户变量"或"系统变量"中找到`Path`，点击"编辑"
3. 添加Flutter的`bin`目录路径，例如：`C:\src\flutter\bin`
4. 点击"确定"保存所有更改

### 1.3 验证Flutter安装
打开**命令提示符**或**PowerShell**，运行：
```bash
flutter --version
```
应该显示Flutter版本信息。

## 第2步：安装Android开发环境

### 2.1 安装Android Studio
1. 下载 [Android Studio](https://developer.android.com/studio)
2. 运行安装程序，使用默认设置
3. 安装完成后启动Android Studio

### 2.2 安装Android SDK
1. 首次启动时，选择"Standard"安装类型
2. 确保勾选以下组件：
   - Android SDK
   - Android SDK Platform
   - Android Virtual Device
3. 点击"Next"完成安装

### 2.3 配置Android环境变量
1. 找到Android SDK安装路径（通常在`C:\Users\你的用户名\AppData\Local\Android\Sdk`）
2. 添加以下环境变量到`Path`：
   - `%ANDROID_HOME%\platform-tools`
   - `%ANDROID_HOME%\tools`
   - `%ANDROID_HOME%\tools\bin`
3. 新建系统变量：
   - 变量名：`ANDROID_HOME`
   - 变量值：Android SDK路径（如`C:\Users\你的用户名\AppData\Local\Android\Sdk`）

## 第3步：接受Android许可证

打开命令提示符，运行：
```bash
flutter doctor --android-licenses
```
按`y`接受所有许可证。

## 第4步：验证开发环境

运行以下命令检查环境：
```bash
flutter doctor
```

**期望的输出**：
```
[✓] Flutter (Channel stable, ...)
[✓] Android toolchain - develop for Android devices
[✓] Chrome - develop for the web
[✓] Visual Studio - develop for Windows
[✓] Connected device
[✓] Network resources
```

如果看到`[!]`或`[✗]`，按照提示解决问题。

## 第5步：初始化Flutter项目

### 5.1 创建平台文件
由于项目只包含Dart代码，需要生成Android/iOS平台文件：
```bash
cd tablet_app
flutter create --platforms=android .
```
这会在当前目录生成Android项目文件，不会覆盖现有代码。

### 5.2 检查项目结构
确保有以下目录结构：
```
tablet_app/
├── android/          # Android项目文件
├── ios/              # iOS项目文件（如需）
├── lib/main.dart     # 主程序代码
└── pubspec.yaml      # 依赖配置
```

## 第6步：准备项目

### 6.1 安装项目依赖
```bash
cd tablet_app
flutter pub get
```

### 6.2 检查依赖
```bash
flutter pub outdated
```
如果有更新，可以运行：
```bash
flutter pub upgrade
```

## 第7步：构建APK

### 7.1 调试版APK（用于测试）
```bash
flutter build apk --debug
```
生成位置：`build/app/outputs/apk/debug/app-debug.apk`

### 7.2 发布版APK（用于分发）
```bash
flutter build apk --release
```
生成位置：`build/app/outputs/apk/release/app-release.apk`

### 7.3 使用构建脚本（推荐）
运行项目根目录的 `build_apk.bat`：
```bash
cd ..
build_apk.bat
```

## 第8步：安装APK到设备

### 8.1 通过USB安装
1. 在Android设备上启用"开发者选项"：
   - 设置 → 关于手机 → 连续点击"版本号"7次
2. 启用"USB调试"：
   - 设置 → 开发者选项 → USB调试
3. 连接设备到电脑
4. 运行安装命令：
```bash
# 安装调试版
flutter install

# 或手动安装
adb install build/app/outputs/apk/release/app-release.apk
```

### 8.2 通过文件传输安装
1. 将APK文件复制到设备（USB、蓝牙、云存储）
2. 在设备上打开文件管理器，找到APK文件
3. 点击安装（可能需要允许"未知来源应用"）

## 第9步：测试应用

### 9.1 基本功能测试
1. 打开应用
2. 点击右上角设置图标
3. 输入PC端IP地址（如`192.168.1.100:8765`）
4. 点击"保存设置"
5. 返回主界面，点击"连接"
6. 测试"启动"和"停止"按钮

### 9.2 网络测试
确保：
1. PC和平板在同一Wi-Fi网络
2. PC防火墙允许端口8765
3. PC端网关软件正在运行

## 常见问题解决

### 问题1：`flutter doctor`显示Android工具链问题
```bash
# 安装缺失的组件
flutter doctor --android-licenses
sdkmanager --update
sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"
```

### 问题2：构建失败，显示Gradle错误
```bash
# 清理项目
flutter clean

# 删除Gradle缓存
rm -rf ~/.gradle/caches/

# 重新获取依赖
flutter pub get

# 重新构建
flutter build apk --release
```

### 问题3：网络超时（中国用户）
```bash
# 设置国内镜像
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn

# 或修改Flutter安装目录下的flutter.gradle文件
# 将google()和jcenter()替换为国内镜像
```

### 问题4：APK安装失败
1. 检查设备存储空间
2. 卸载旧版本：`adb uninstall com.example.tablet_modbus_controller`
3. 启用"未知来源应用"权限

## 构建优化

### 减小APK大小
```bash
flutter build apk --release --split-per-abi
```
这会生成三个APK，分别针对不同CPU架构：
- `app-armeabi-v7a-release.apk`（32位）
- `app-arm64-v8a-release.apk`（64位，推荐）
- `app-x86_64-release.apk`（模拟器）

### 添加应用图标
1. 准备图标文件（1024x1024 PNG）
2. 放在 `tablet_app/assets/` 目录
3. 在 `pubspec.yaml` 中配置：
```yaml
flutter:
  assets:
    - assets/icon.png
```

## 下一步

### 发布到应用商店
1. 生成应用签名密钥
2. 配置签名信息
3. 构建发布版APK
4. 提交到Google Play Store

### 功能扩展
1. 添加更多控制按钮
2. 实现寄存器值显示
3. 添加历史记录功能
4. 支持多设备连接

## 获取帮助

- [Flutter官方文档](https://flutter.dev/docs)
- [Flutter中文网](https://flutter.cn)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/flutter)

## 版本历史
- v1.0.0: 初始版本，支持基本Modbus控制
- 构建日期: 2026-04-22