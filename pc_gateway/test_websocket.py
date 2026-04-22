#!/usr/bin/env python3
"""
WebSocket连接测试脚本
用于测试PC端WebSocket服务器是否正常工作
"""

import asyncio
import websockets
import sys

async def test_connection():
    """测试WebSocket连接"""
    uri = "ws://192.168.0.127:8765"

    print(f"尝试连接到: {uri}")
    print("注意: 请确保PC端网关正在运行 (python main.py)")
    print("-" * 50)

    try:
        # 设置较短的超时时间（新版本使用open_timeout）
        async with websockets.connect(uri, open_timeout=5) as websocket:
            print("✅ 连接成功!")

            # 接收欢迎消息
            welcome = await websocket.recv()
            print(f"收到欢迎消息: {welcome}")

            # 发送测试命令
            test_command = '{"command": "status"}'
            print(f"发送命令: {test_command}")
            await websocket.send(test_command)

            # 接收响应
            response = await websocket.recv()
            print(f"收到响应: {response}")

            print("\n✅ WebSocket服务器工作正常!")
            return True

    except asyncio.TimeoutError:
        print("❌ 连接超时 (5秒)")
        print("可能原因:")
        print("1. PC端网关未运行")
        print("2. 防火墙阻止了端口8765")
        print("3. IP地址错误")
        return False

    except ConnectionRefusedError:
        print("❌ 连接被拒绝")
        print("可能原因:")
        print("1. WebSocket服务器未启动")
        print("2. 端口8765未被监听")
        return False

    except Exception as e:
        print(f"❌ 连接失败: {type(e).__name__}: {e}")
        return False

def test_port():
    """测试端口是否开放"""
    import socket
    print("\n" + "="*50)
    print("测试端口8765是否开放...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)

    try:
        result = sock.connect_ex(('192.168.0.127', 8765))
        if result == 0:
            print("✅ 端口8765已开放")
        else:
            print(f"❌ 端口8765未开放 (错误码: {result})")
            print("请检查:")
            print("1. 是否运行了 'python main.py'?")
            print("2. 是否点击了'启动WebSocket服务器'按钮?")
            print("3. Windows防火墙是否允许端口8765?")
        sock.close()
        return result == 0
    except Exception as e:
        print(f"❌ 端口测试失败: {e}")
        return False

def check_firewall():
    """检查防火墙设置"""
    print("\n" + "="*50)
    print("防火墙检查:")
    print("1. 打开'控制面板' → 'Windows Defender防火墙'")
    print("2. 点击'高级设置'")
    print("3. 选择'入站规则'")
    print("4. 查找是否有规则允许端口8765")
    print("5. 如果没有，需要新建规则:")
    print("   - 规则类型: 端口")
    print("   - 协议: TCP")
    print("   - 端口: 8765")
    print("   - 操作: 允许连接")
    print("   - 配置文件: 全部勾选")
    print("   - 名称: 'Modbus WebSocket'")

async def main():
    print("="*50)
    print("WebSocket连接诊断工具")
    print("="*50)

    # 测试端口
    port_open = test_port()

    if not port_open:
        check_firewall()
        return

    # 测试WebSocket连接
    print("\n" + "="*50)
    print("测试WebSocket连接...")
    success = await test_connection()

    if success:
        print("\n✅ 所有测试通过!")
        print("手机应该可以连接了")
        print("在手机App中填写: 192.168.0.127:8765")
    else:
        print("\n❌ 测试失败")
        print("\n下一步:")
        print("1. 检查PC端网关是否正在运行")
        print("2. 确认点击了'启动WebSocket服务器'按钮")
        print("3. 检查PC端日志是否有错误")
        print("4. 尝试关闭防火墙临时测试")

if __name__ == "__main__":
    # 运行异步测试
    asyncio.run(main())

    print("\n" + "="*50)
    print("按Enter键退出...")
    input()