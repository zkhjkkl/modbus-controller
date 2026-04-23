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
        self._is_connected = False
        # 是否启用地址转换（将40001转换为0）
        self.address_offset = self.config.get("address_offset", 0)

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
            self._is_connected = self.client.connect()
            if self._is_connected:
                logger.info(f"Modbus连接成功: {self.config}")
            else:
                logger.error(f"Modbus连接失败: {self.config}")

            return self._is_connected

        except Exception as e:
            logger.error(f"连接Modbus设备时出错: {str(e)}")
            self._is_connected = False
            return False

    def disconnect(self):
        """断开连接"""
        if self.client:
            self.client.close()
            self._is_connected = False
            logger.info("Modbus连接已关闭")

    def write_register(self, register, value, slave_id=None, register_type="coil"):
        """
        写寄存器

        Args:
            register: 寄存器地址
            value: 写入的值
            slave_id: 从站ID，默认为配置中的slave_id
            register_type: 寄存器类型，支持：
                - 'coil': 写单个线圈 (功能码0x05)
                - 'holding_register': 写单个保持寄存器 (功能码0x06)
                - 'coils': 写多个线圈 (功能码0x0F) - value应为列表
                - 'holding_registers': 写多个保持寄存器 (功能码0x10) - value应为列表

        Returns:
            bool: 是否成功
        """
        if not self._is_connected:
            logger.error("Modbus未连接")
            return False

        slave_id = slave_id or self.config.get("slave_id", 1)

        # 地址转换
        original_address = register
        register = self.convert_address(register)
        logger.debug(f"写操作地址转换: {original_address} -> {register}")

        try:
            if register_type == "coil":
                # 写单个线圈 (功能码0x05)
                result = self.client.write_coil(
                    address=register,
                    value=bool(value),
                    slave=slave_id
                )
            elif register_type == "holding_register":
                # 写单个保持寄存器 (功能码0x06)
                result = self.client.write_register(
                    address=register,
                    value=value,
                    slave=slave_id
                )
            elif register_type == "coils":
                # 写多个线圈 (功能码0x0F)
                if not isinstance(value, list):
                    value = [bool(value)]
                result = self.client.write_coils(
                    address=register,
                    values=[bool(v) for v in value],
                    slave=slave_id
                )
            elif register_type == "holding_registers":
                # 写多个保持寄存器 (功能码0x10)
                if not isinstance(value, list):
                    value = [value]
                result = self.client.write_registers(
                    address=register,
                    values=value,
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
            register_type: 寄存器类型，支持：
                - 'coil': 读线圈 (功能码0x01)
                - 'discrete_input': 读离散输入 (功能码0x02)
                - 'holding_register': 读保持寄存器 (功能码0x03)
                - 'input_register': 读输入寄存器 (功能码0x04)

        Returns:
            list: 读取的值列表，失败返回None
        """
        if not self._is_connected:
            logger.error("Modbus未连接")
            return None

        slave_id = slave_id or self.config.get("slave_id", 1)

        # 地址转换
        original_address = register
        register = self.convert_address(register)
        logger.debug(f"读操作地址转换: {original_address} -> {register}")

        try:
            if register_type == "coil":
                # 读线圈 (功能码0x01)
                result = self.client.read_coils(
                    address=register,
                    count=count,
                    slave=slave_id
                )
            elif register_type == "discrete_input":
                # 读离散输入 (功能码0x02)
                result = self.client.read_discrete_inputs(
                    address=register,
                    count=count,
                    slave=slave_id
                )
            elif register_type == "holding_register":
                # 读保持寄存器 (功能码0x03)
                result = self.client.read_holding_registers(
                    address=register,
                    count=count,
                    slave=slave_id
                )
            elif register_type == "input_register":
                # 读输入寄存器 (功能码0x04)
                result = self.client.read_input_registers(
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
                # 根据结果类型提取值
                if hasattr(result, 'registers'):
                    values = list(result.registers)
                elif hasattr(result, 'bits'):
                    values = list(result.bits)
                else:
                    values = []

                logger.info(f"读寄存器成功: 地址={register}, 值={values}, 类型={register_type}")
                return values

        except ModbusException as e:
            logger.error(f"Modbus异常: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"读寄存器时出错: {str(e)}")
            return None

    def convert_address(self, address):
        """
        转换Modbus地址

        Args:
            address: 原始地址（如40001）

        Returns:
            int: 转换后的地址
        """
        # 自动检测并转换常见的Modbus地址映射
        if address >= 40000 and address <= 49999:
            # 保持寄存器：40001-49999 -> 0-9998
            converted = address - 40001
            logger.debug(f"地址转换: {address} (保持寄存器) -> {converted}")
            return converted
        elif address >= 30000 and address <= 39999:
            # 输入寄存器：30001-39999 -> 0-9998
            converted = address - 30001
            logger.debug(f"地址转换: {address} (输入寄存器) -> {converted}")
            return converted
        elif address >= 10000 and address <= 19999:
            # 离散输入：10001-19999 -> 0-9998
            converted = address - 10001
            logger.debug(f"地址转换: {address} (离散输入) -> {converted}")
            return converted
        elif address >= 0 and address <= 9999:
            # 线圈：00001-09999 -> 0-9998
            converted = address - 1
            logger.debug(f"地址转换: {address} (线圈) -> {converted}")
            return converted
        else:
            # 已经是转换后的地址或无效地址
            return address

    def is_connected(self):
        """检查是否连接"""
        return self._is_connected and self.client is not None