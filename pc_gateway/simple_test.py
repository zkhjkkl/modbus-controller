#!/usr/bin/env python3
"""
简单的WebSocket连接测试
"""

import asyncio
import websockets

async def simple_test():
    uri = "ws://192.168.0.127:8765"

    print(f"测试连接到: {uri}")
    print("使用最简单的连接方式...")

    try:
        # 使用最简单的连接，不指定超时
        async with websockets.connect(uri) as websocket:
            print("✅ 连接成功!")

            # 尝试接收消息
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=2)
                print(f"收到消息: {message}")
            except asyncio.TimeoutError:
                print("⚠️  没有收到消息（可能正常）")

            # 发送简单消息
            await websocket.send('{"command": "status"}')

            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=2)
                print(f"收到响应: {response}")
            except asyncio.TimeoutError:
                print("⚠️  没有收到响应（可能正常）")

            print("✅ 测试完成!")
            return True

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ HTTP状态码错误: {e}")
        print("可能原因: WebSocket服务器未正确响应")
        return False
    except websockets.exceptions.InvalidHandshake as e:
        print(f"❌ 握手失败: {e}")
        print("可能原因: 服务器不是WebSocket服务器，或协议不匹配")
        return False
    except ConnectionRefusedError:
        print("❌ 连接被拒绝")
        print("可能原因: 服务器未运行，或防火墙阻止")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {type(e).__name__}: {e}")
        return False

def check_server_status():
    """检查服务器状态"""
    import socket
    print("\n" + "="*50)
    print("检查服务器状态...")

    # 检查端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        result = sock.connect_ex(('192.168.0.127', 8765))
        if result == 0:
            print("✅ 端口8765已开放")

            # 尝试发送一个简单的HTTP请求
            sock.send(b"GET / HTTP/1.1\r\nHost: 192.168.0.127:8765\r\n\r\n")

            try:
                response = sock.recv(1024)
                print(f"服务器响应: {response[:100]}...")
            except socket.timeout:
                print("⚠️  服务器未响应HTTP请求（WebSocket服务器正常）")
            except Exception as e:
                print(f"⚠️  读取响应失败: {e}")

        else:
            print(f"❌ 端口8765未开放 (错误码: {result})")
        sock.close()
        return result == 0
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("简单WebSocket测试")
    print("="*50)

    # 检查服务器
    server_up = check_server_status()

    if server_up:
        print("\n" + "="*50)
        print("测试WebSocket连接...")
        asyncio.run(simple_test())
    else:
        print("\n❌ 服务器未运行，无法测试WebSocket")

    print("\n" + "="*50)
    print("诊断完成")
    print("="*50)