"""
Modbus客户端封装
支持TCP和RTU模式
"""

import logging
from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.exceptions import ModbusException

logger = logging.getLogger(__name__)

class ModbusClient:
    """Modbus客户端"""

    def __init__(self, config):
        """
        初始化Modbus客户端

        Args:
            config: 配置字典，包含mode, host, port, slave_id等
        """
        self.config = config
        self.client = None
        self.is_connected = False

    def connect(self):
        """连接Modbus设备"""
        try:
            mode = self.config.get("mode", "tcp")

            if mode == "tcp":
                self.client = ModbusTcpClient(
                    host=self.config.get("host", "127.0.0.1"),
                    port=self.config.get("port", 502)
                )
            elif mode == "rtu":
                self.client = ModbusSerialClient(
                    port=self.config.get("serial_port", "COM1"),
                    baudrate=self.config.get("baudrate", 9600),
                    parity=self.config.get("parity", "N"),
                    stopbits=self.config.get("stopbits", 1),
                    bytesize=self.config.get("bytesize", 8)
                )
            else:
                raise ValueError(f"不支持的Modbus模式: {mode}")

            # 尝试连接
            self.is_connected = self.client.connect()
            if self.is_connected:
                logger.info(f"Modbus连接成功: {self.config}")
            else:
                logger.error(f"Modbus连接失败: {self.config}")

            return self.is_connected

        except Exception as e:
            logger.error(f"连接Modbus设备时出错: {str(e)}")
            self.is_connected = False
            return False

    def disconnect(self):
        """断开连接"""
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info("Modbus连接已关闭")

    def write_register(self, register, value, slave_id=None, register_type="coil"):
        """
        写寄存器

        Args:
            register: 寄存器地址
            value: 写入的值
            slave_id: 从站ID，默认为配置中的slave_id
            register_type: 寄存器类型，'coil'或'holding_register'

        Returns:
            bool: 是否成功
        """
        if not self.is_connected:
            logger.error("Modbus未连接")
            return False

        slave_id = slave_id or self.config.get("slave_id", 1)

        try:
            if register_type == "coil":
                # 写线圈
                result = self.client.write_coil(
                    address=register,
                    value=bool(value),
                    slave=slave_id
                )
            elif register_type == "holding_register":
                # 写保持寄存器
                result = self.client.write_register(
                    address=register,
                    value=value,
                    slave=slave_id
                )
            else:
                logger.error(f"不支持的寄存器类型: {register_type}")
                return False

            if result.isError():
                logger.error(f"写寄存器失败: {result}")
                return False
            else:
                logger.info(f"写寄存器成功: 地址={register}, 值={value}, 类型={register_type}")
                return True

        except ModbusException as e:
            logger.error(f"Modbus异常: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"写寄存器时出错: {str(e)}")
            return False

    def read_register(self, register, count=1, slave_id=None, register_type="holding_register"):
        """
        读寄存器

        Args:
            register: 寄存器地址
            count: 读取数量
            slave_id: 从站ID
            register_type: 寄存器类型

        Returns:
            list: 读取的值列表，失败返回None
        """
        if not self.is_connected:
            logger.error("Modbus未连接")
            return None

        slave_id = slave_id or self.config.get("slave_id", 1)

        try:
            if register_type == "coil":
                # 读线圈
                result = self.client.read_coils(
                    address=register,
                    count=count,
                    slave=slave_id
                )
            elif register_type == "holding_register":
                # 读保持寄存器
                result = self.client.read_holding_registers(
                    address=register,
                    count=count,
                    slave=slave_id
                )
            else:
                logger.error(f"不支持的寄存器类型: {register_type}")
                return None

            if result.isError():
                logger.error(f"读寄存器失败: {result}")
                return None
            else:
                values = list(result.registers) if hasattr(result, 'registers') else list(result.bits)
                logger.info(f"读寄存器成功: 地址={register}, 值={values}")
                return values

        except ModbusException as e:
            logger.error(f"Modbus异常: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"读寄存器时出错: {str(e)}")
            return None

    def is_connected(self):
        """检查是否连接"""
        return self.is_connected and self.client is not None