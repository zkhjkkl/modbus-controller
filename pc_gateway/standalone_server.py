#!/usr/bin/env python3
"""
独立WebSocket服务器测试
不通过GUI，直接运行WebSocket服务器
"""

import asyncio
import json
import logging
import websockets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleWebSocketServer:
    """简单的WebSocket服务器"""

    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.clients = set()

    async def handler(self, websocket, path):
        """处理客户端连接"""
        client_ip = websocket.remote_address[0]
        logger.info(f"客户端连接: {client_ip}")
        self.clients.add(websocket)

        try:
            # 发送欢迎消息
            welcome = {
                "type": "welcome",
                "message": "连接到测试服务器"
            }
            await websocket.send(json.dumps(welcome))

            # 监听消息
            async for message in websocket:
                logger.info(f"收到消息: {message}")

                try:
                    data = json.loads(message)
                    await self.process_command(data, websocket)
                except json.JSONDecodeError:
                    error_msg = {"status": "error", "message": "无效的JSON格式"}
                    await websocket.send(json.dumps(error_msg))
                except Exception as e:
                    error_msg = {"status": "error", "message": str(e)}
                    await websocket.send(json.dumps(error_msg))

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"客户端断开连接: {client_ip}")
        finally:
            self.clients.remove(websocket)

    async def process_command(self, data, websocket):
        """处理命令"""
        command = data.get("command")

        if command == "status":
            response = {
                "status": "ok",
                "message": "服务器运行正常",
                "server": "standalone"
            }
            await websocket.send(json.dumps(response))
        elif command == "ping":
            response = {"status": "ok", "message": "pong"}
            await websocket.send(json.dumps(response))
        else:
            response = {"status": "error", "message": f"未知命令: {command}"}
            await websocket.send(json.dumps(response))

    async def run_server(self):
        """运行服务器"""
        async with websockets.serve(self.handler, self.host, self.port):
            logger.info(f"WebSocket服务器启动: {self.host}:{self.port}")
            await asyncio.Future()  # 永久运行

async def test_client():
    """测试客户端"""
    await asyncio.sleep(1)  # 等待服务器启动

    uri = "ws://localhost:8765"

    try:
        async with websockets.connect(uri) as ws:
            print("测试客户端连接成功!")

            # 接收欢迎消息
            welcome = await ws.recv()
            print(f"收到欢迎消息: {welcome}")

            # 发送测试命令
            await ws.send('{"command": "status"}')
            response = await ws.recv()
            print(f"收到响应: {response}")

            return True
    except Exception as e:
        print(f"测试客户端失败: {e}")
        return False

async def main():
    """主函数"""
    print("=" * 50)
    print("独立WebSocket服务器测试")
    print("=" * 50)

    # 创建服务器
    server = SimpleWebSocketServer("0.0.0.0", 8765)

    # 启动服务器任务
    server_task = asyncio.create_task(server.run_server())

    # 等待服务器启动
    await asyncio.sleep(1)

    # 测试连接
    print("\n测试本地连接...")
    success = await test_client()

    if success:
        print("\n✅ 服务器运行正常!")
        print(f"手机可以连接: 192.168.0.127:8765")
        print("按 Ctrl+C 停止服务器")

        # 保持运行
        try:
            await server_task
        except asyncio.CancelledError:
            print("服务器已停止")
    else:
        print("\n❌ 服务器测试失败")
        server_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止")