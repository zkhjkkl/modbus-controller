# 快速开始指南

## 选择方案

### 方案1：HTTP + 网页界面（推荐，最简单）
- **PC端**：Flask网页服务器
- **平板端**：任何现代浏览器
- **优点**：零平板端部署，跨平台，开发最快
- **快速开始**：
  ```bash
  cd pc_gateway
  python app.py
  ```
  然后在平板浏览器访问 `http://<PC_IP>:5000`

### 方案2：WebSocket + Flutter应用（原方案）
- **PC端**：PyQt GUI + WebSocket服务器
- **平板端**：Flutter应用（需安装APK）
- **优点**：原生应用体验，离线可用
- **快速开始**：继续阅读下文

## 方案2：5分钟快速构建APK

### 前提条件
- Windows 10/11 64位
- 已安装Flutter SDK（如未安装，见下文）
- Android设备或模拟器

### 如果尚未安装Flutter
1. 下载Flutter SDK：https://flutter.dev/docs/get-started/install/windows
2. 解压到 `C:\src\flutter`（不要有中文路径）
3. 添加 `C:\src\flutter\bin` 到系统PATH
4. 运行 `flutter doctor` 检查环境

### 快速构建步骤

#### 步骤1：初始化项目
```bash
# 在项目根目录运行
init_project.bat
```

#### 步骤2：构建APK
```bash
# 在项目根目录运行
build_apk.bat
```

#### 步骤3：安装APK
```bash
# 方法1：通过USB（设备需启用USB调试）
adb install tablet_app\build\app\outputs\apk\release\app-release.apk

# 方法2：复制APK文件到设备手动安装
```

#### 步骤4：配置和使用
1. 确保PC端网关正在运行（`python main.py`）
2. 在平板应用设置中输入PC的IP地址（如 `192.168.1.100:8765`）
3. 点击"连接"按钮
4. 使用"启动"/"停止"按钮控制设备

### 一键脚本
如果你已经安装Flutter，可以运行：
```bash
# 完整流程（初始化+构建）
init_project.bat && build_apk.bat
```

### 常见快捷命令
```bash
# 直接运行到设备（开发模式）
cd tablet_app
flutter run

# 构建调试版APK
flutter build apk --debug

# 清理项目
flutter clean

# 检查依赖更新
flutter pub upgrade
```

### 网络配置要点
1. **PC和平板必须在同一Wi-Fi网络**
2. **PC防火墙允许端口8765**
3. **获取PC的IP地址**：
   ```bash
   # Windows
   ipconfig
   # 查找 IPv4 地址，如 192.168.1.100
   ```

### 故障快速排查
1. **连接失败**：检查PC防火墙，确认网关正在运行
2. **构建失败**：运行 `flutter clean` 然后重试
3. **安装失败**：设备启用"USB调试"和"未知来源应用"
4. **按钮无响应**：检查Modbus设备连接和寄存器地址

### 获取帮助
- 详细指南：`BUILD_GUIDE.md`
- 安装说明：`docs/INSTALL.md`
- 项目文档：`README.md`

---

## 精简版步骤（已安装Flutter）
```bash
# 1. 初始化
init_project.bat

# 2. 构建
build_apk.bat

# 3. 安装
adb install tablet_app\build\app\outputs\apk\release\app-release.apk

# 4. 运行PC端网关
cd pc_gateway
python main.py

# 5. 在平板应用设置PC IP，点击连接
```

## 测试成功标志
1. 平板应用显示"已连接"
2. 点击"启动"按钮，PC端日志显示写寄存器成功
3. Modbus设备响应控制命令

---

**提示**：首次构建可能需要10-20分钟（下载依赖），后续构建只需1-2分钟。