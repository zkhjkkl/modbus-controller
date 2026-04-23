#!/usr/bin/env python3
"""
Modbus HTTP网关 - Flask版本
提供网页界面控制Modbus设备
"""

import json
import logging
import sys
import os
import socket
from flask import Flask, render_template, request, jsonify, send_from_directory

# 添加当前目录到Python路径，确保可以导入modbus_client
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modbus_client import ModbusClient

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 设置modbus_client日志级别为DEBUG
logging.getLogger('modbus_client').setLevel(logging.DEBUG)

# 创建Flask应用
app = Flask(__name__)

# 全局变量
modbus_client = None
config = None
mappings = None

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        # 创建一个UDP套接字连接到外部地址来获取本地IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到公共DNS服务器，但不发送数据
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            # 备选方法：获取主机名对应的IP
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if ip.startswith("127."):
                # 如果是回环地址，返回localhost
                return "127.0.0.1"
            return ip
        except Exception:
            return "127.0.0.1"

def load_config():
    """加载配置文件"""
    global config, mappings
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            config = config_data.get('modbus', {})
            mappings = config_data.get('mappings', {})
            logger.info(f"配置文件加载成功: {config_path}")
            logger.info(f"Modbus配置: {config}")
            logger.info(f"按钮映射: {mappings}")
            return True
    except FileNotFoundError:
        logger.error(f"配置文件不存在: {config_path}")
        # 创建默认配置
        default_config = {
            "modbus": {
                "mode": "tcp",
                "host": "192.168.1.100",
                "port": 502,
                "slave_id": 1
            },
            "mappings": {
                "start": {
                    "register": 40001,
                    "value": 1,
                    "type": "coil"
                },
                "stop": {
                    "register": 40002,
                    "value": 0,
                    "type": "coil"
                }
            }
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        logger.info(f"已创建默认配置文件: {config_path}")
        config = default_config['modbus']
        mappings = default_config['mappings']
        return True
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        return False

def connect_modbus():
    """连接Modbus设备"""
    global modbus_client
    try:
        modbus_client = ModbusClient(config)
        if modbus_client.connect():
            logger.info("Modbus连接成功")
            return True
        else:
            logger.error("Modbus连接失败")
            return False
    except Exception as e:
        logger.error(f"连接Modbus设备时出错: {str(e)}")
        return False

@app.route('/')
def index():
    """主页面 - 显示控制界面"""
    status = {
        'modbus_connected': modbus_client.is_connected() if modbus_client else False,
        'config': config,
        'mappings': mappings
    }
    return render_template('index.html', status=status)

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    status = {
        'modbus_connected': modbus_client.is_connected() if modbus_client else False,
        'config': config,
        'mappings': mappings
    }
    return jsonify(status)

@app.route('/api/connect', methods=['POST'])
def connect():
    """连接Modbus设备"""
    if modbus_client and modbus_client.is_connected():
        return jsonify({'status': 'ok', 'message': 'Modbus已连接'})

    success = connect_modbus()
    if success:
        return jsonify({'status': 'ok', 'message': 'Modbus连接成功'})
    else:
        return jsonify({'status': 'error', 'message': 'Modbus连接失败'}), 500

@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    """断开Modbus连接"""
    global modbus_client
    if modbus_client:
        modbus_client.disconnect()
        modbus_client = None
        logger.info("Modbus连接已断开")
        return jsonify({'status': 'ok', 'message': 'Modbus连接已断开'})
    else:
        return jsonify({'status': 'ok', 'message': 'Modbus未连接'})

@app.route('/api/write', methods=['POST'])
def write_register():
    """写寄存器API"""
    if not modbus_client or not modbus_client.is_connected():
        return jsonify({'status': 'error', 'message': 'Modbus未连接'}), 400

    data = request.json
    if not data:
        return jsonify({'status': 'error', 'message': '请求数据为空'}), 400

    register = data.get('register')
    value = data.get('value')
    register_type = data.get('type', 'coil')
    slave_id = data.get('slave_id')

    if register is None or value is None:
        return jsonify({'status': 'error', 'message': '缺少寄存器地址或值'}), 400

    try:
        success = modbus_client.write_register(
            register=register,
            value=value,
            slave_id=slave_id,
            register_type=register_type
        )
        if success:
            return jsonify({'status': 'ok', 'message': '写寄存器成功'})
        else:
            return jsonify({'status': 'error', 'message': '写寄存器失败'}), 500
    except Exception as e:
        logger.error(f"写寄存器时出错: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/read', methods=['POST'])
def read_register():
    """读寄存器API"""
    if not modbus_client or not modbus_client.is_connected():
        return jsonify({'status': 'error', 'message': 'Modbus未连接'}), 400

    data = request.json
    if not data:
        return jsonify({'status': 'error', 'message': '请求数据为空'}), 400

    register = data.get('register')
    count = data.get('count', 1)
    register_type = data.get('type', 'holding_register')
    slave_id = data.get('slave_id')

    if register is None:
        return jsonify({'status': 'error', 'message': '缺少寄存器地址'}), 400

    try:
        values = modbus_client.read_register(
            register=register,
            count=count,
            slave_id=slave_id,
            register_type=register_type
        )
        if values is not None:
            return jsonify({'status': 'ok', 'values': values})
        else:
            return jsonify({'status': 'error', 'message': '读寄存器失败'}), 500
    except Exception as e:
        logger.error(f"读寄存器时出错: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/command/<command_name>', methods=['POST'])
def execute_command(command_name):
    """执行预定义命令（如start, stop）"""
    if not modbus_client or not modbus_client.is_connected():
        return jsonify({'status': 'error', 'message': 'Modbus未连接'}), 400

    if command_name not in mappings:
        return jsonify({'status': 'error', 'message': f'未找到命令: {command_name}'}), 404

    mapping = mappings[command_name]
    try:
        success = modbus_client.write_register(
            register=mapping['register'],
            value=mapping['value'],
            register_type=mapping.get('type', 'coil')
        )
        if success:
            return jsonify({'status': 'ok', 'message': f'{command_name}命令执行成功'})
        else:
            return jsonify({'status': 'error', 'message': f'{command_name}命令执行失败'}), 500
    except Exception as e:
        logger.error(f"执行命令{command_name}时出错: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test_connection():
    """测试Modbus连接和基本功能"""
    if not modbus_client or not modbus_client.is_connected():
        return jsonify({'status': 'error', 'message': 'Modbus未连接'}), 400

    test_results = []

    try:
        # 测试1: 读取保持寄存器（功能码0x03）
        logger.info("测试1: 读取保持寄存器 (功能码0x03)")
        values = modbus_client.read_register(
            register=0,  # 测试地址0
            count=1,
            register_type='holding_register'
        )
        if values is not None:
            test_results.append({'test': 'read_holding_register', 'status': 'ok', 'values': values})
        else:
            test_results.append({'test': 'read_holding_register', 'status': 'error', 'message': '读取失败'})

        # 测试2: 读取输入寄存器（功能码0x04）
        logger.info("测试2: 读取输入寄存器 (功能码0x04)")
        values = modbus_client.read_register(
            register=0,  # 测试地址0
            count=1,
            register_type='input_register'
        )
        if values is not None:
            test_results.append({'test': 'read_input_register', 'status': 'ok', 'values': values})
        else:
            test_results.append({'test': 'read_input_register', 'status': 'error', 'message': '读取失败'})

        # 测试3: 读取线圈（功能码0x01）
        logger.info("测试3: 读取线圈 (功能码0x01)")
        values = modbus_client.read_register(
            register=0,  # 测试地址0
            count=1,
            register_type='coil'
        )
        if values is not None:
            test_results.append({'test': 'read_coil', 'status': 'ok', 'values': values})
        else:
            test_results.append({'test': 'read_coil', 'status': 'error', 'message': '读取失败'})

        # 测试4: 读取离散输入（功能码0x02）
        logger.info("测试4: 读取离散输入 (功能码0x02)")
        values = modbus_client.read_register(
            register=0,  # 测试地址0
            count=1,
            register_type='discrete_input'
        )
        if values is not None:
            test_results.append({'test': 'read_discrete_input', 'status': 'ok', 'values': values})
        else:
            test_results.append({'test': 'read_discrete_input', 'status': 'error', 'message': '读取失败'})

        return jsonify({
            'status': 'ok',
            'message': '测试完成',
            'results': test_results
        })

    except Exception as e:
        logger.error(f"测试过程中出错: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'测试失败: {str(e)}',
            'results': test_results
        }), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    return jsonify({
        'status': 'ok',
        'config': config,
        'mappings': mappings
    })

@app.route('/api/config', methods=['POST'])
def save_config():
    """保存配置"""
    global config, mappings, modbus_client

    data = request.json
    if not data:
        return jsonify({'status': 'error', 'message': '请求数据为空'}), 400

    try:
        # 更新配置
        new_config = data.get('config', {})
        new_mappings = data.get('mappings', {})

        # 验证必要字段
        if not new_config.get('host') or not new_config.get('port'):
            return jsonify({'status': 'error', 'message': 'IP地址和端口不能为空'}), 400

        # 更新全局变量
        config.update(new_config)
        mappings.update(new_mappings)

        # 确保配置完整
        config.setdefault('mode', 'tcp')
        config.setdefault('slave_id', 1)

        # 保存到文件
        config_data = {
            'modbus': config,
            'mappings': mappings
        }

        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)

        logger.info(f"配置已保存: {config}")

        # 如果Modbus已连接，重新连接
        if modbus_client and modbus_client.is_connected():
            modbus_client.disconnect()
            modbus_client = None
            logger.info("已断开旧连接，需要重新连接")

        return jsonify({'status': 'ok', 'message': '配置保存成功'})

    except Exception as e:
        logger.error(f"保存配置失败: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """提供静态文件"""
    return send_from_directory('static', filename)

def init_app():
    """初始化应用"""
    # 加载配置
    if not load_config():
        logger.error("初始化失败: 无法加载配置")
        return False

    # 连接Modbus
    connect_modbus()

    return True

if __name__ == '__main__':
    # 初始化应用
    if init_app():
        # 获取本机IP地址
        local_ip = get_local_ip()

        logger.info("Modbus HTTP网关启动中...")
        logger.info("请访问 http://localhost:5000 使用控制界面")
        logger.info(f"平板端可访问 http://{local_ip}:5000")

        # 打印显眼的连接提示
        print("\n" + "="*60)
        print(" "*20 + "移动设备连接提示")
        print("="*60)
        print("请使用手机或平板浏览器访问以下地址：")
        print("")
        print(f"    http://{local_ip}:5000")
        print("")
        print("确保手机/平板与电脑在同一局域网内")
        print("="*60 + "\n")

        # 启动Flask开发服务器
        # 注意: 生产环境应使用生产服务器如gunicorn
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.error("应用初始化失败，退出")
        sys.exit(1)