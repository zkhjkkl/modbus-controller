#!/usr/bin/env python3
"""
最简单的WebSocket Echo服务器
用于测试WebSocket基本功能
"""

import asyncio
import websockets

async def echo_handler(websocket, path):
    """简单的echo处理器"""
    print(f"客户端连接: {websocket.remote_address}")

    try:
        # 发送欢迎消息
        await websocket.send('{"type": "welcome", "message": "Echo server"}')

        # 接收并回显消息
        async for message in websocket:
            print(f"收到消息: {message}")
            # 简单回显
            await websocket.send(f'{{"echo": "{message}"}}')

    except websockets.exceptions.ConnectionClosed:
        print(f"客户端断开: {websocket.remote_address}")

async def main():
    """主函数"""
    print("=" * 50)
    print("简单WebSocket Echo服务器")
    print("监听端口: 8766 (避免与8765冲突)")
    print("=" * 50)

    # 使用8766端口，避免与原有服务器冲突
    server = await websockets.serve(echo_handler, "0.0.0.0", 8766)

    print("服务器已启动!")
    print("手机可以连接: 192.168.0.127:8766")
    print("按 Ctrl+C 停止服务器")

    # 保持运行
    await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止")