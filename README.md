# 平板无线Modbus控制系统

## 项目概述
开发两个软件实现平板电脑无线控制Modbus设备：
1. **平板端应用**：安装在平板（Android/iOS）上，提供启动/停止按钮
2. **PC端网关软件**：安装在PC上，负责Modbus通信和转发平板指令

## 系统架构
```
平板应用 (Flutter) ↔ WebSocket ↔ PC网关 (Python) ↔ Modbus TCP/RTU ↔ 工业设备
```

## 技术栈
- **平板端**：Flutter 3.x (Dart)，使用web_socket_channel库
- **PC端**：Python 3.9+，PyQt6 (GUI)，pymodbus (Modbus)，websockets (WebSocket服务器)
- **通信协议**：WebSocket (JSON消息格式)

## 功能说明

### PC端网关软件
1. **Modbus连接配置**
   - 支持TCP和RTU模式
   - 配置从站地址、寄存器地址、数据类型
2. **按钮映射配置**
   - 将启动按钮映射到指定寄存器地址和值
   - 将停止按钮映射到指定寄存器地址和值
3. **WebSocket服务器**
   - 监听平板连接（默认端口8765）
   - 接收控制命令并执行Modbus写操作
4. **GUI界面**
   - 连接状态显示
   - 配置面板
   - 操作日志

### 平板端应用
1. **连接配置**
   - 输入PC的IP地址和端口
2. **控制界面**
   - 大型启动/停止按钮
   - 连接状态指示
3. **通信**
   - WebSocket连接PC网关
   - 发送JSON格式控制命令

## 通信协议
### WebSocket消息格式
**平板 → PC (控制命令)**
```json
{
  "command": "write",
  "register": 40001,
  "value": 1,
  "type": "coil"
}
```

**PC →平板 (响应)**
```json
{
  "status": "ok",
  "message": "Write successful"
}
```

## 项目结构
```
project/
├── tablet_app/          # Flutter平板应用
│   ├── lib/
│   │   └── main.dart
│   └── pubspec.yaml
├── pc_gateway/          # PC网关软件
│   ├── main.py
│   ├── modbus_client.py
│   ├── websocket_server.py
│   └── config.json
└── docs/               # 文档
```

## 快速开始
### PC端安装
```bash
cd pc_gateway
pip install -r requirements.txt
python main.py
```

### 平板端安装
```bash
cd tablet_app
flutter pub get
flutter run
```

## 配置示例
### Modbus配置 (config.json)
```json
{
  "modbus": {
    "mode": "tcp",
    "host": "192.168.1.100",
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

## 构建APK（平板端应用）

### 快速构建
1. **初始化项目**：运行 `init_project.bat`
2. **构建APK**：运行 `build_apk.bat`
3. **安装APK**：将生成的APK文件安装到Android设备

### 详细指南
- [快速开始指南](QUICK_START.md) - 5分钟快速构建
- [完整构建指南](BUILD_GUIDE.md) - 详细步骤和故障排除
- [安装说明](docs/INSTALL.md) - 系统安装和配置

### 生成的APK文件
- 发布版：`tablet_app/build/app/outputs/apk/release/app-release.apk`
- 调试版：`tablet_app/build/app/outputs/apk/debug/app-debug.apk`

## 下一步
1. 安装开发环境（Flutter SDK, Python, PyQt6）
2. 运行PC端网关软件：`cd pc_gateway && python main.py`
3. 构建平板端APK：运行 `build_apk.bat`
4. 安装APK到平板设备
5. 配置网络连接，测试控制功能