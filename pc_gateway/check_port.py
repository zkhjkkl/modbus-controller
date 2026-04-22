#!/usr/bin/env python3
"""
检查端口是否开放
"""

import socket
import sys

def check_port(host="192.168.0.127", port=8766):
    """检查端口是否开放"""
    print(f"检查端口: {host}:{port}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"端口 {port} 已开放")

            # 尝试读取数据
            try:
                sock.send(b"GET / HTTP/1.1\r\n\r\n")
                data = sock.recv(1024)
                print(f"服务器响应: {data[:100]}")
            except socket.timeout:
                print("服务器无响应（可能正常）")
            except Exception as e:
                print(f"读取响应错误: {e}")

            return True
        else:
            print(f"端口 {port} 未开放 (错误码: {result})")
            return False
    except Exception as e:
        print(f"检查错误: {e}")
        return False
    finally:
        sock.close()

def check_all_ports():
    """检查所有相关端口"""
    ports = [8766, 8765, 8080, 8888, 80]

    for port in ports:
        print(f"\n{'='*50}")
        print(f"检查端口 {port}")
        print('='*50)

        if check_port(port=port):
            print(f"✅ 端口 {port} 可用")
        else:
            print(f"❌ 端口 {port} 不可用")

if __name__ == "__main__":
    print("端口检查工具")
    print("=" * 50)

    # 检查8766端口（echo服务器）
    print("检查Echo服务器端口 (8766)...")
    if not check_port(port=8766):
        print("\nEcho服务器未运行!")
        print("请运行: python simple_echo_server.py")

    # 检查8765端口（原服务器）
    print("\n" + "="*50)
    print("检查原服务器端口 (8765)...")
    if not check_port(port=8765):
        print("\n原服务器未运行!")
        print("请运行: python main.py 并点击'启动WebSocket服务器'")

    print("\n" + "="*50)
    print("检查完成")