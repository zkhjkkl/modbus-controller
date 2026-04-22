# 安装指南

## 系统要求

### PC端网关软件
- Windows 10/11 或 Linux 或 macOS
- Python 3.9 或更高版本
- 网络连接（用于与平板通信）
- Modbus设备（PLC等）

### 平板端应用
- Android 8.0+ 或 iOS 13.0+
- Flutter开发环境（仅开发需要）
- 无线网络（与PC在同一局域网）

## PC端安装步骤

### 1. 安装Python
从 [python.org](https://www.python.org) 下载并安装Python 3.9+

### 2. 安装依赖
```bash
cd pc_gateway
pip install -r requirements.txt
```

### 3. 配置Modbus连接
编辑 `config.json` 文件：
```json
{
  "modbus": {
    "mode": "tcp",
    "host": "你的设备IP",
    "port": 502,
    "slave_id": 1
  },
  "mappings": {
    "start": {
      "register": 40001,
      "value": 1,
      "type": "coil"
    },
    "stop": {
      "register": 40002,
      "value": 0,
      "type": "coil"
    }
  }
}
```

### 4. 运行网关软件
```bash
python main.py
```

### 5. 配置防火墙
确保端口8765在防火墙中开放：
- Windows: 允许Python通过防火墙
- Linux: `sudo ufw allow 8765`

## 平板端安装步骤

### 选项1：直接安装APK（Android）
1. 在PC端编译APK：
```bash
cd tablet_app
flutter build apk --release
```
2. 将 `build/app/outputs/apk/release/app-release.apk` 复制到平板
3. 在平板上安装APK（需允许未知来源安装）

### 选项2：通过Flutter开发环境安装
1. 安装Flutter SDK: [flutter.dev](https://flutter.dev)
2. 连接平板到电脑（USB调试模式）
3. 运行应用：
```bash
cd tablet_app
flutter run
```

### 选项3：iOS安装（需要Apple开发者账号）
1. 编译IPA：
```bash
flutter build ios --release
```
2. 通过Xcode部署到设备

## 网络配置

### 1. 确保PC和平板在同一网络
- PC和平板连接到同一个Wi-Fi网络
- 获取PC的IP地址：
  - Windows: `ipconfig`
  - Linux/macOS: `ifconfig`

### 2. 配置平板应用
1. 打开平板应用
2. 点击右上角设置图标
3. 输入PC的IP地址和端口（例如: `192.168.1.100:8765`）
4. 点击保存

### 3. 测试连接
1. 在平板上点击"连接"按钮
2. 状态应显示"已连接"
3. 点击启动/停止按钮测试控制

## 故障排除

### 连接问题
1. **平板无法连接PC**
   - 检查PC防火墙设置
   - 确认PC和平板在同一网络
   - 重启PC端网关软件

2. **Modbus连接失败**
   - 检查Modbus设备电源和网络
   - 确认IP地址和端口正确
   - 检查从站ID设置

3. **按钮操作无响应**
   - 检查寄存器地址是否正确
   - 确认寄存器类型（线圈/保持寄存器）
   - 查看PC端日志信息

### 常见错误
- **"Connection refused"**: PC端网关未运行或端口被占用
- **"Timeout"**: 网络延迟或设备无响应
- **"Modbus exception"**: 寄存器地址无效或设备忙

## 高级配置

### 自定义寄存器映射
在 `config.json` 中修改 `mappings` 部分：
```json
"mappings": {
  "start": {
    "register": 40001,
    "value": 1,
    "type": "coil"
  },
  "stop": {
    "register": 40002,
    "value": 0,
    "type": "holding_register"
  }
}
```

### 多设备支持
可以运行多个网关实例，使用不同端口：
```bash
# 实例1
python main.py --port 8765

# 实例2
python main.py --port 8766
```

### 安全配置
1. 修改WebSocket端口
2. 添加身份验证（需修改代码）
3. 使用VPN确保网络安全

## 更新日志
- v1.0.0: 初始版本，支持基本Modbus控制和无线连接