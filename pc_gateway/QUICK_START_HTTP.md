# HTTP网关快速启动指南

## 方案概述
使用Flask提供网页界面，平板通过浏览器访问，无需安装任何应用：
```
平板浏览器 → HTTP请求 → Flask服务器 (PC端) → Modbus设备
```

## 安装步骤

### 1. 安装Python依赖
```bash
pip install -r requirements-http.txt
```
或使用启动脚本自动安装。

### 2. 配置Modbus连接
编辑 `config.json` 文件：
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

### 3. 启动HTTP网关
```bash
python app.py
```
或使用启动脚本：
- Windows: 双击 `run_http_gateway.bat`
- Linux/Mac: `./run_http_gateway.sh`

### 4. 获取PC IP地址
```bash
ipconfig  # Windows
ifconfig  # Linux/Mac
```
查找 **IPv4 地址**（如 `192.168.31.45`）

## 平板端使用

### 1. 连接平板
1. 确保平板和PC在同一网络
2. 在平板浏览器中访问：`http://<PC_IP地址>:5000`
   - 例如：`http://192.168.31.45:5000`
3. 网页将自动加载控制界面

### 2. 使用控制界面
1. **连接Modbus**：点击"连接Modbus"按钮
2. **控制设备**：使用"启动设备"和"停止设备"按钮
3. **手动控制**：在"手动控制"区域读写寄存器
4. **查看日志**：操作日志实时显示在下方

## 网页功能说明

### 状态面板
- Modbus连接状态（绿色=已连接，红色=未连接）
- 按钮映射配置显示
- 访问信息（PC端和平板端URL）

### 控制按钮
- **连接Modbus**：建立Modbus连接
- **断开连接**：断开Modbus连接
- **启动设备**：执行启动映射（寄存器40001=1）
- **停止设备**：执行停止映射（寄存器40002=0）

### 手动控制
- **寄存器地址**：0-65535
- **值**：0-65535
- **寄存器类型**：线圈(Coil)或保持寄存器(Holding Register)
- **从站ID**：可选，默认使用配置中的slave_id
- **写入寄存器**：将值写入指定寄存器
- **读取寄存器**：读取指定寄存器的值

### 操作日志
- 实时显示所有操作结果
- 不同颜色表示不同级别（信息、成功、错误）
- 自动滚动，最多保留50条记录

## 配置文件详解

### Modbus配置
```json
"modbus": {
  "mode": "tcp",           // 连接模式：tcp 或 rtu
  "host": "192.168.1.100", // TCP模式：设备IP地址
  "port": 502,             // TCP模式：端口号
  "slave_id": 1,           // 从站ID：1-247
  // RTU模式额外参数：
  "serial_port": "COM1",   // 串口：COM1, COM2, ...
  "baudrate": 9600,        // 波特率：9600, 19200, ...
  "parity": "N",           // 校验位：N, E, O
  "stopbits": 1,           // 停止位：1, 1.5, 2
  "bytesize": 8            // 数据位：8
}
```

### 按钮映射配置
```json
"mappings": {
  "start": {
    "register": 40001,     // 启动寄存器地址
    "value": 1,            // 启动值
    "type": "coil"         // 寄存器类型：coil 或 holding_register
  },
  "stop": {
    "register": 40002,     // 停止寄存器地址
    "value": 0,            // 停止值
    "type": "coil"         // 寄存器类型
  }
}
```

## 防火墙配置（如连接失败）
以管理员身份运行PowerShell：
```powershell
New-NetFirewallRule -DisplayName "Modbus HTTP Gateway" `
  -Direction Inbound -LocalPort 5000 `
  -Protocol TCP -Action Allow
```

## 启动脚本说明

### Windows (`run_http_gateway.bat`)
- 自动检查Python安装
- 自动安装依赖
- 启动Flask服务器
- 显示访问URL

### Linux/Mac (`run_http_gateway.sh`)
- 检查Python3安装
- 安装依赖
- 启动Flask服务器
- 显示访问URL

## 故障排除

### 1. 无法访问网页
- 确认防火墙已放行端口5000
- 确认PC和平板在同一网络
- 检查Flask服务器是否正常运行
- 查看命令行错误信息

### 2. Modbus连接失败
- 检查 `config.json` 中的设备配置
- 确认Modbus设备电源和网络连接正常
- 检查设备IP地址和端口是否正确
- 查看Flask日志中的错误信息

### 3. 按钮操作无响应
- 确认Modbus已连接（状态显示绿色）
- 检查按钮映射配置是否正确
- 查看操作日志中的错误信息
- 尝试手动读写寄存器测试

### 4. 依赖安装失败
- 确保Python 3.6+已安装
- 尝试使用管理员权限运行
- 手动安装：`pip install Flask pymodbus`

## 高级功能

### 1. 自定义端口
修改 `app.py` 最后一行：
```python
app.run(host='0.0.0.0', port=8080, debug=False)  # 修改端口号
```

### 2. 生产环境部署
开发服务器不适合生产环境，建议使用：
- **gunicorn** (Linux/Mac): `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- **waitress** (Windows): `waitress-serve --port=5000 app:app`

### 3. 多设备支持
修改 `config.json` 添加更多映射：
```json
"mappings": {
  "start": {...},
  "stop": {...},
  "reset": {
    "register": 40003,
    "value": 1,
    "type": "coil"
  }
}
```
然后在网页手动控制区域使用API调用。

## API接口
HTTP网关提供以下API接口：

| 端点 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 网页控制界面 |
| `/api/status` | GET | 获取系统状态 |
| `/api/connect` | POST | 连接Modbus设备 |
| `/api/disconnect` | POST | 断开Modbus连接 |
| `/api/write` | POST | 写寄存器 |
| `/api/read` | POST | 读寄存器 |
| `/api/command/<name>` | POST | 执行预定义命令 |

## 推荐流程
1. 运行 `run_http_gateway.bat` (Windows) 或 `./run_http_gateway.sh` (Linux/Mac)
2. 获取PC IP地址
3. 在平板浏览器访问 `http://<PC_IP>:5000`
4. 点击"连接Modbus"按钮
5. 使用"启动设备"/"停止设备"按钮控制