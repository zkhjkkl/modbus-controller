"""
WebSocket服务器
接收平板端控制命令，转发到Modbus设备
"""

import asyncio
import json
import logging
from PyQt6.QtCore import QObject, pyqtSignal
import websockets

logger = logging.getLogger(__name__)

class WebSocketServer(QObject):
    """WebSocket服务器"""

    message_received = pyqtSignal(str)  # 信号：收到消息

    def __init__(self, host="0.0.0.0", port=8765, modbus_client=None, mappings=None):
        super().__init__()
        self.host = host
        self.port = port
        self.modbus_client = modbus_client
        self.mappings = mappings or {}
        self.server = None
        self.clients = set()
        self.running = False

    async def handler(self, websocket, path):
        """处理客户端连接"""
        client_ip = websocket.remote_address[0]
        logger.info(f"客户端连接: {client_ip}")
        self.clients.add(websocket)

        try:
            # 发送欢迎消息
            welcome = {
                "type": "welcome",
                "message": "连接到Modbus网关",
                "mappings": self.mappings
            }
            await websocket.send(json.dumps(welcome))

            # 监听消息
            async for message in websocket:
                logger.info(f"收到消息: {message}")
                self.message_received.emit(message)

                try:
                    # 解析JSON消息
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
        """
        处理控制命令

        Args:
            data: 命令数据字典
            websocket: 客户端连接
        """
        command = data.get("command")

        if command == "write":
            # 直接写寄存器命令
            register = data.get("register")
            value = data.get("value")
            register_type = data.get("type", "coil")

            if register is None or value is None:
                response = {"status": "error", "message": "缺少寄存器地址或值"}
                await websocket.send(json.dumps(response))
                return

            if self.modbus_client and self.modbus_client.is_connected():
                success = self.modbus_client.write_register(
                    register=register,
                    value=value,
                    register_type=register_type
                )
                if success:
                    response = {"status": "ok", "message": "写寄存器成功"}
                else:
                    response = {"status": "error", "message": "写寄存器失败"}
            else:
                response = {"status": "error", "message": "Modbus未连接"}

            await websocket.send(json.dumps(response))

        elif command == "start":
            # 启动命令 - 使用映射配置
            await self.execute_mapping("start", websocket)

        elif command == "stop":
            # 停止命令 - 使用映射配置
            await self.execute_mapping("stop", websocket)

        elif command == "status":
            # 状态查询
            status = {
                "status": "ok",
                "modbus_connected": self.modbus_client.is_connected() if self.modbus_client else False,
                "mappings": self.mappings
            }
            await websocket.send(json.dumps(status))

        else:
            response = {"status": "error", "message": f"未知命令: {command}"}
            await websocket.send(json.dumps(response))

    async def execute_mapping(self, mapping_name, websocket):
        """执行映射命令"""
        if mapping_name not in self.mappings:
            response = {"status": "error", "message": f"未找到映射: {mapping_name}"}
            await websocket.send(json.dumps(response))
            return

        mapping = self.mappings[mapping_name]

        if self.modbus_client and self.modbus_client.is_connected():
            success = self.modbus_client.write_register(
                register=mapping["register"],
                value=mapping["value"],
                register_type=mapping.get("type", "coil")
            )
            if success:
                response = {"status": "ok", "message": f"{mapping_name}命令执行成功"}
            else:
                response = {"status": "error", "message": f"{mapping_name}命令执行失败"}
        else:
            response = {"status": "error", "message": "Modbus未连接"}

        await websocket.send(json.dumps(response))

    async def run_server(self):
        """运行WebSocket服务器"""
        self.running = True
        try:
            async with websockets.serve(self.handler, self.host, self.port):
                logger.info(f"WebSocket服务器启动: {self.host}:{self.port}")
                await asyncio.Future()  # 永久运行
        except Exception as e:
            logger.error(f"WebSocket服务器错误: {str(e)}")
        finally:
            self.running = False

    def start(self):
        """启动服务器（在QThread中调用）"""
        asyncio.run(self.run_server())

    def stop(self):
        """停止服务器"""
        self.running = False
        # 关闭所有客户端连接
        for client in self.clients:
            asyncio.create_task(client.close())
        logger.info("WebSocket服务器已停止")

    async def broadcast(self, message):
        """广播消息给所有客户端"""
        if self.clients:
            await asyncio.gather(
                *[client.send(message) for client in self.clients]
            )