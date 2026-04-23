# PC端网关快速启动指南

## 问题诊断
Python 3.14.4 已安装，但未添加到系统 PATH 环境变量。

## 解决方案（三选一）

### 方案1：使用完整路径（最简单，推荐）
无需修改系统设置。

1. **安装依赖**：
   ```powershell
   .\install_with_full_path.bat
   ```

2. **运行网关**：
   ```powershell
   .\run_with_full_path.bat
   ```
   或双击 `run_with_full_path.bat`

### 方案2：修复PATH（一劳永逸）
将Python添加到PATH，以后可以直接使用 `python` 命令。

1. **运行修复工具**：
   ```powershell
   .\fix_python_path.bat
   ```
   按照提示操作。

2. **安装依赖**：
   ```powershell
   python -m pip install -r requirements.txt
   ```

3. **运行网关**：
   ```powershell
   python main.py
   ```

### 方案3：手动操作
1. **使用完整路径安装**：
   ```powershell
   "C:\Users\BRT252\AppData\Local\Programs\Python\Python314\python.exe" -m pip install -r requirements.txt
   ```

2. **使用完整路径运行**：
   ```powershell
   "C:\Users\BRT252\AppData\Local\Programs\Python\Python314\python.exe" main.py
   ```

## 安装后步骤

### 1. 获取PC IP地址
```powershell
ipconfig
```
查找 **IPv4 地址**（如 `192.168.31.45`）

### 2. 配置平板应用
- 打开平板Modbus控制器应用
- 点击右上角设置图标
- 输入服务器地址：`你的IP:8765`
- 例如：`192.168.31.45:8765`
- 点击保存

### 3. 测试连接
1. 在平板上点击"连接"按钮
2. 状态应显示"已连接"
3. 点击启动/停止按钮测试控制

## 防火墙配置（如连接失败）
以管理员身份运行PowerShell：
```powershell
New-NetFirewallRule -DisplayName "Modbus Gateway" `
  -Direction Inbound -LocalPort 8765 `
  -Protocol TCP -Action Allow
```

## 文件说明

| 文件 | 用途 |
|------|------|
| `install_with_full_path.bat` | 使用完整路径安装依赖 |
| `run_with_full_path.bat` | 使用完整路径运行网关 |
| `fix_python_path.bat` | 修复Python PATH问题 |
| `test_python_simple.bat` | 测试Python安装状态 |

## 推荐流程
1. 运行 `.\install_with_full_path.bat` 安装依赖
2. 运行 `.\run_with_full_path.bat` 启动网关
3. 获取PC IP地址，配置平板连接

## 故障排除

### 安装失败
- 以管理员身份运行脚本
- 检查网络连接
- 手动安装：`"C:\Users\BRT252\AppData\Local\Programs\Python\Python314\python.exe" -m pip install PyQt6 pymodbus websockets`

### 连接失败
- 确认PC和平板在同一Wi-Fi网络
- 检查防火墙设置
- 重启网关程序

### 网关启动失败
- 确保Python 3.14.4已安装
- 检查 `config.json` 中的Modbus设备配置
- 查看错误日志信息