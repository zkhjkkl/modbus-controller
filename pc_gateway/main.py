#!/usr/bin/env python3
"""
PC端Modbus网关主程序
提供GUI配置Modbus连接和按钮映射，运行WebSocket服务器接收平板指令
"""

import sys
import json
import logging
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGroupBox, QLabel, QLineEdit,
                             QPushButton, QTextEdit, QTabWidget, QComboBox,
                             QSpinBox, QFormLayout, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont

from modbus_client import ModbusClient
from websocket_server_fixed import WebSocketServerFixed as WebSocketServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModbusConfigWidget(QWidget):
    """Modbus配置界面"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        # 连接模式
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["TCP", "RTU"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        layout.addRow("连接模式:", self.mode_combo)

        # TCP配置
        self.host_edit = QLineEdit("192.168.1.100")
        layout.addRow("主机地址:", self.host_edit)

        self.port_edit = QSpinBox()
        self.port_edit.setRange(1, 65535)
        self.port_edit.setValue(502)
        layout.addRow("端口:", self.port_edit)

        # RTU配置（默认隐藏）
        self.rtu_group = QGroupBox("RTU设置")
        rtu_layout = QFormLayout()
        self.serial_port_edit = QLineEdit("COM1")
        rtu_layout.addRow("串口:", self.serial_port_edit)
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(["9600", "19200", "38400", "57600", "115200"])
        rtu_layout.addRow("波特率:", self.baudrate_combo)
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(["N", "E", "O"])
        rtu_layout.addRow("校验位:", self.parity_combo)
        self.rtu_group.setLayout(rtu_layout)
        self.rtu_group.setVisible(False)
        layout.addRow(self.rtu_group)

        # 从站ID
        self.slave_id_spin = QSpinBox()
        self.slave_id_spin.setRange(1, 247)
        self.slave_id_spin.setValue(1)
        layout.addRow("从站ID:", self.slave_id_spin)

        # 连接按钮
        self.connect_btn = QPushButton("连接")
        self.connect_btn.clicked.connect(self.on_connect)
        layout.addRow(self.connect_btn)

        self.setLayout(layout)

    def on_mode_changed(self, mode):
        """切换TCP/RTU模式"""
        self.rtu_group.setVisible(mode == "RTU")

    def on_connect(self):
        """连接Modbus设备"""
        # 实际连接逻辑在MainWindow中实现
        pass

    def get_config(self):
        """获取配置字典"""
        config = {
            "mode": self.mode_combo.currentText().lower(),
            "host": self.host_edit.text(),
            "port": self.port_edit.value(),
            "slave_id": self.slave_id_spin.value()
        }
        if config["mode"] == "rtu":
            config.update({
                "serial_port": self.serial_port_edit.text(),
                "baudrate": int(self.baudrate_combo.currentText()),
                "parity": self.parity_combo.currentText()
            })
        return config

class ButtonMappingWidget(QWidget):
    """按钮映射配置界面"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        # 启动按钮映射
        self.start_register_spin = QSpinBox()
        self.start_register_spin.setRange(0, 65535)
        self.start_register_spin.setValue(40001)
        layout.addRow("启动寄存器地址:", self.start_register_spin)

        self.start_value_spin = QSpinBox()
        self.start_value_spin.setRange(0, 65535)
        self.start_value_spin.setValue(1)
        layout.addRow("启动值:", self.start_value_spin)

        self.start_type_combo = QComboBox()
        self.start_type_combo.addItems(["coil", "holding_register"])
        layout.addRow("启动数据类型:", self.start_type_combo)

        # 分隔线
        layout.addRow(QLabel(""))

        # 停止按钮映射
        self.stop_register_spin = QSpinBox()
        self.stop_register_spin.setRange(0, 65535)
        self.stop_register_spin.setValue(40002)
        layout.addRow("停止寄存器地址:", self.stop_register_spin)

        self.stop_value_spin = QSpinBox()
        self.stop_value_spin.setRange(0, 65535)
        self.stop_value_spin.setValue(0)
        layout.addRow("停止值:", self.stop_value_spin)

        self.stop_type_combo = QComboBox()
        self.stop_type_combo.addItems(["coil", "holding_register"])
        layout.addRow("停止数据类型:", self.stop_type_combo)

        # 保存按钮
        self.save_btn = QPushButton("保存映射")
        layout.addRow(self.save_btn)

        self.setLayout(layout)

    def get_mappings(self):
        """获取映射配置"""
        return {
            "start": {
                "register": self.start_register_spin.value(),
                "value": self.start_value_spin.value(),
                "type": self.start_type_combo.currentText()
            },
            "stop": {
                "register": self.stop_register_spin.value(),
                "value": self.stop_value_spin.value(),
                "type": self.stop_type_combo.currentText()
            }
        }

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.modbus_client = None
        self.websocket_server = None
        self.init_ui()
        self.load_config()

    def init_ui(self):
        self.setWindowTitle("Modbus无线网关 v1.0")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # 状态栏
        status_layout = QHBoxLayout()
        self.status_label = QLabel("状态: 未连接")
        self.status_label.setStyleSheet("font-weight: bold; color: red;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        # WebSocket服务器控制
        self.ws_toggle_btn = QPushButton("启动WebSocket服务器")
        self.ws_toggle_btn.clicked.connect(self.toggle_websocket_server)
        status_layout.addWidget(self.ws_toggle_btn)

        main_layout.addLayout(status_layout)

        # 选项卡
        self.tabs = QTabWidget()

        # Modbus配置标签
        self.modbus_widget = ModbusConfigWidget()
        self.modbus_widget.connect_btn.clicked.connect(self.connect_modbus)
        self.tabs.addTab(self.modbus_widget, "Modbus配置")

        # 按钮映射标签
        self.mapping_widget = ButtonMappingWidget()
        self.mapping_widget.save_btn.clicked.connect(self.save_mappings)
        self.tabs.addTab(self.mapping_widget, "按钮映射")

        main_layout.addWidget(self.tabs)

        # 日志显示
        log_group = QGroupBox("操作日志")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        central_widget.setLayout(main_layout)

        # 定时器更新状态
        from PyQt6.QtCore import QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)

    def log_message(self, message):
        """添加日志消息"""
        self.log_text.append(message)
        logger.info(message)

    def connect_modbus(self):
        """连接Modbus设备"""
        config = self.modbus_widget.get_config()

        try:
            self.modbus_client = ModbusClient(config)
            if self.modbus_client.connect():
                self.status_label.setText("状态: Modbus已连接")
                self.status_label.setStyleSheet("font-weight: bold; color: green;")
                self.log_message(f"Modbus连接成功: {config}")
            else:
                self.log_message("Modbus连接失败")
        except Exception as e:
            self.log_message(f"连接错误: {str(e)}")

    def save_mappings(self):
        """保存按钮映射配置"""
        mappings = self.mapping_widget.get_mappings()
        config = {
            "modbus": self.modbus_widget.get_config(),
            "mappings": mappings
        }

        try:
            with open("config.json", "w") as f:
                json.dump(config, f, indent=2)
            self.log_message("配置已保存到 config.json")
        except Exception as e:
            self.log_message(f"保存配置失败: {str(e)}")

    def load_config(self):
        """加载配置文件"""
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                # TODO: 加载配置到UI
                self.log_message("配置已加载")
        except FileNotFoundError:
            self.log_message("未找到配置文件，使用默认配置")
        except Exception as e:
            self.log_message(f"加载配置失败: {str(e)}")

    def toggle_websocket_server(self):
        """启动/停止WebSocket服务器"""
        if self.websocket_server is None:
            # 启动服务器
            self.websocket_server = WebSocketServer(
                host="0.0.0.0",
                port=8765,
                modbus_client=self.modbus_client,
                mappings=self.mapping_widget.get_mappings()
            )
            self.websocket_server.message_received.connect(self.handle_ws_message)
            self.websocket_server.start()

            self.ws_toggle_btn.setText("停止WebSocket服务器")
            self.log_message("WebSocket服务器已启动 (端口: 8765)")
        else:
            # 停止服务器
            self.websocket_server.stop()
            self.websocket_server = None

            self.ws_toggle_btn.setText("启动WebSocket服务器")
            self.log_message("WebSocket服务器已停止")

    def handle_ws_message(self, message):
        """处理WebSocket消息"""
        self.log_message(f"收到消息: {message}")

    def update_status(self):
        """更新状态显示"""
        if self.modbus_client and self.modbus_client.is_connected():
            self.status_label.setText("状态: Modbus已连接")
            self.status_label.setStyleSheet("font-weight: bold; color: green;")
        else:
            self.status_label.setText("状态: Modbus未连接")
            self.status_label.setStyleSheet("font-weight: bold; color: red;")

    def closeEvent(self, event):
        """关闭窗口事件"""
        if self.websocket_server:
            self.websocket_server.stop()
        if self.modbus_client:
            self.modbus_client.disconnect()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()