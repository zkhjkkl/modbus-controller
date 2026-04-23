# Modbus HTTP网关 - 打包指南

## 概述

本文档介绍如何将Modbus HTTP网关打包成独立的EXE文件，方便分发给没有Python环境的用户使用。

## 打包前提条件

1. **Python 3.6+** - 打包机器需要安装Python
2. **网络连接** - 用于下载依赖包

## 打包步骤

### 方法一：使用打包脚本（推荐）

1. 双击运行 `build_exe.bat`
2. 脚本会自动：
   - 检查Python环境
   - 安装PyInstaller和依赖
   - 打包生成EXE文件
3. 打包完成后，EXE文件位于 `dist\ModbusHTTPGateway.exe`

### 方法二：手动打包

1. 安装依赖：
   ```cmd
   pip install -r requirements-http.txt
   pip install pyinstaller
   ```

2. 执行打包命令：
   ```cmd
   pyinstaller --onefile ^
       --name "ModbusHTTPGateway" ^
       --add-data "static;static" ^
       --add-data "templates;templates" ^
       --add-data "config.json;." ^
       --clean ^
       app.py
   ```

3. 生成的EXE文件在 `dist` 目录中

## 文件结构

打包时需要包含以下文件：
- `app.py` - 主程序
- `modbus_client.py` - Modbus客户端
- `config.json` - 配置文件
- `templates/index.html` - 网页界面
- `static/` - 静态文件目录（当前为空）

## 分发使用

### 单文件分发
将 `dist\ModbusHTTPGateway.exe` 单独复制到目标电脑即可运行。

### 完整目录分发
如果需要保留配置文件的可编辑性，可以分发以下文件结构：
```
ModbusHTTPGateway/
├── ModbusHTTPGateway.exe
├── config.json          （可修改配置文件）
├── templates/
│   └── index.html
└── static/              （空目录）
```

## 运行说明

### 运行EXE文件
1. 双击 `ModbusHTTPGateway.exe`
2. 控制台窗口会显示启动信息
3. 访问提示的URL地址：
   - 电脑端：http://localhost:5000
   - 手机/平板：http://<电脑IP>:5000

### 防火墙设置
首次运行时，Windows防火墙可能会阻止访问。请允许程序通过防火墙，或手动开放5000端口。

## 常见问题

### 1. 打包时出现"未找到Python"错误
- 确保已安装Python 3.6+
- 将Python添加到系统PATH环境变量
- 或使用完整路径运行Python：`C:\Python39\python.exe`

### 2. EXE文件运行后无法访问网页
- 检查防火墙设置
- 确保没有其他程序占用5000端口
- 查看控制台输出的错误信息

### 3. 配置文件修改后不生效
- 单文件EXE：配置文件被打包在EXE内部，运行时解压到临时目录
- 如需修改配置，建议使用完整目录分发方式，直接修改外部的config.json

### 4. 杀毒软件误报
某些杀毒软件可能将PyInstaller打包的程序误报为病毒。可以：
- 将EXE文件添加到杀毒软件白名单
- 使用代码签名证书签名EXE文件
- 在打包机器上排除误报

## 高级选项

### 隐藏控制台窗口
如果希望运行时不显示控制台窗口，在打包命令中添加 `--noconsole` 参数：
```cmd
pyinstaller --onefile --noconsole --name "ModbusHTTPGateway" ...
```

### 自定义图标
为EXE文件添加图标：
```cmd
pyinstaller --onefile --icon=app.ico --name "ModbusHTTPGateway" ...
```

### 减小文件体积
使用UPX压缩（需要先下载UPX）：
```cmd
pyinstaller --onefile --upx-dir="C:\upx" --name "ModbusHTTPGateway" ...
```

## 技术支持

如有问题，请检查：
1. 控制台输出的错误信息
2. 查看 `build` 目录中的日志文件
3. 确保所有依赖包已正确安装