#!/usr/bin/env python3
"""
HTTP网关测试脚本
检查依赖和基本功能
"""

import sys
import os
import json

def check_python_version():
    """检查Python版本"""
    print("1. 检查Python版本...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("   ❌ 需要Python 3.6或更高版本")
        return False
    else:
        print("   ✅ Python版本符合要求")
        return True

def check_dependencies():
    """检查依赖包"""
    print("\n2. 检查依赖包...")

    dependencies = ['Flask', 'pymodbus']
    missing = []

    for dep in dependencies:
        try:
            __import__(dep.lower() if dep == 'Flask' else dep)
            print(f"   ✅ {dep} 已安装")
        except ImportError:
            print(f"   ❌ {dep} 未安装")
            missing.append(dep)

    if missing:
        print(f"\n   安装缺失依赖: pip install {' '.join(missing)}")
        return False
    else:
        print("   ✅ 所有依赖已安装")
        return True

def check_config_file():
    """检查配置文件"""
    print("\n3. 检查配置文件...")

    config_path = 'config.json'
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            # 检查必要字段
            required = ['modbus', 'mappings']
            for req in required:
                if req not in config:
                    print(f"   ❌ 配置缺少 '{req}' 字段")
                    return False

            print("   ✅ 配置文件格式正确")
            print(f"   Modbus模式: {config['modbus'].get('mode', '未设置')}")
            print(f"   按钮映射: {list(config['mappings'].keys())}")
            return True

        except json.JSONDecodeError as e:
            print(f"   ❌ 配置文件JSON格式错误: {e}")
            return False
        except Exception as e:
            print(f"   ❌ 读取配置文件失败: {e}")
            return False
    else:
        print("   ⚠️  配置文件不存在，将使用默认配置")
        return True

def check_modbus_client():
    """检查Modbus客户端模块"""
    print("\n4. 检查Modbus客户端模块...")

    try:
        # 尝试导入modbus_client
        sys.path.append('.')
        from modbus_client import ModbusClient

        print("   ✅ Modbus客户端模块可导入")

        # 测试创建实例
        test_config = {
            "mode": "tcp",
            "host": "127.0.0.1",
            "port": 502,
            "slave_id": 1
        }

        client = ModbusClient(test_config)
        print("   ✅ Modbus客户端实例创建成功")

        # 注意：不实际连接，只是测试导入
        return True

    except ImportError as e:
        print(f"   ❌ 无法导入modbus_client: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Modbus客户端测试失败: {e}")
        return False

def check_flask_app():
    """检查Flask应用"""
    print("\n5. 检查Flask应用...")

    try:
        # 尝试导入app模块但不运行
        sys.path.append('.')

        # 模拟Flask环境
        import flask
        print("   ✅ Flask可导入")

        # 检查模板目录
        if os.path.exists('templates') and os.path.exists('templates/index.html'):
            print("   ✅ 模板文件存在")
        else:
            print("   ❌ 模板目录或文件缺失")
            return False

        return True

    except ImportError as e:
        print(f"   ❌ Flask导入失败: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Flask检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Modbus HTTP网关测试")
    print("=" * 50)

    tests = [
        check_python_version,
        check_dependencies,
        check_config_file,
        check_modbus_client,
        check_flask_app
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ 测试异常: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    for i, result in enumerate(results):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"测试{i+1}: {status}")

    print(f"\n总计: {passed}/{total} 项测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！可以启动HTTP网关:")
        print("   运行: python app.py")
        print("   访问: http://localhost:5000")
        return 0
    else:
        print("\n⚠️  部分测试失败，请修复问题后再运行")
        print("   常见解决方案:")
        print("   1. 安装依赖: pip install -r requirements-http.txt")
        print("   2. 检查配置文件 config.json")
        print("   3. 确保所有文件在正确位置")
        return 1

if __name__ == "__main__":
    sys.exit(main())