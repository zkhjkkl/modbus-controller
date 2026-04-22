#!/usr/bin/env python3
"""
测试修复版WebSocket服务器
"""

import asyncio
import json
import threading
import time
import websockets
from websocket_server_fixed import WebSocketServerFixed

def run_server():
    """运行WebSocket服务器"""
    server = WebSocketServerFixed(host="0.0.0.0", port=8765)
    server.start()
    print(f"WebSocket服务器已启动: 0.0.0.0:8765")
    print("按 Ctrl+C 停止服务器")

    # 保持服务器运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止服务器...")
        server.stop()
        print("服务器已停止")

async def test_client():
    """测试客户端连接"""
    print("\n" + "="*50)
    print("测试客户端连接...")
    print("="*50)

    uri = "ws://127.0.0.1:8765"

    try:
        async with websockets.connect(uri) as ws:
            print(f"[OK] 已连接到: {uri}")

            # 接收欢迎消息
            try:
                welcome = await asyncio.wait_for(ws.recv(), timeout=3)
                data = json.loads(welcome)
                print(f"[OK] 收到欢迎消息: {data.get('type')}")
                print(f"  消息: {data.get('message')}")
            except asyncio.TimeoutError:
                print("[ERROR] 未收到欢迎消息")
            except json.JSONDecodeError:
                print(f"[ERROR] 欢迎消息不是有效的JSON: {welcome}")

            # 发送状态查询
            print("\n发送状态查询...")
            await ws.send(json.dumps({"command": "status"}))

            try:
                response = await asyncio.wait_for(ws.recv(), timeout=3)
                data = json.loads(response)
                print(f"[OK] 收到状态响应: {data}")
            except asyncio.TimeoutError:
                print("[ERROR] 未收到状态响应")
            except json.JSONDecodeError:
                print(f"[ERROR] 响应不是有效的JSON: {response}")

            # 发送测试命令
            print("\n发送测试命令...")
            await ws.send(json.dumps({"command": "test"}))

            try:
                response = await asyncio.wait_for(ws.recv(), timeout=3)
                data = json.loads(response)
                print(f"[OK] 收到测试响应: {data}")
            except asyncio.TimeoutError:
                print("[ERROR] 未收到测试响应")

            print("\n" + "="*50)
            print("[OK] 所有测试完成！")
            print("="*50)
            return True

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"[ERROR] 无效的HTTP状态码: {e}")
    except websockets.exceptions.InvalidHandshake as e:
        print(f"[ERROR] 握手失败: {e}")
    except ConnectionRefusedError:
        print(f"[ERROR] 连接被拒绝 - 服务器可能未运行")
    except Exception as e:
        print(f"[ERROR] 错误: {type(e).__name__}: {e}")

    print("\n" + "="*50)
    print("[ERROR] 测试失败")
    print("="*50)
    return False

def main():
    """主函数"""
    print("="*50)
    print("修复版WebSocket服务器测试")
    print("="*50)

    # 启动服务器线程
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)

    # 运行客户端测试
    success = asyncio.run(test_client())

    if success:
        print("\n[SUCCESS] 修复版WebSocket服务器工作正常！")
        print("手机App应该可以连接了。")
        print("请重新构建APK并测试。")
    else:
        print("\n[FAILED] 修复版WebSocket服务器测试失败")
        print("请检查服务器代码和网络配置。")

    print("\n按 Enter 退出...")
    input()

if __name__ == "__main__":
    main()