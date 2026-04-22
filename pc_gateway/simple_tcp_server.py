#!/usr/bin/env python3
"""
最简单的TCP服务器
用于测试端口是否真的在监听
"""

import socket
import threading
import time

def handle_client(client_socket, address):
    """处理客户端连接"""
    print(f"客户端连接: {address}")

    try:
        # 读取数据
        data = client_socket.recv(1024)
        if data:
            print(f"收到数据: {data[:100]}")

            # 简单响应
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from TCP server"
            client_socket.send(response)
    except Exception as e:
        print(f"处理客户端错误: {e}")
    finally:
        client_socket.close()
        print(f"客户端断开: {address}")

def start_tcp_server(host="0.0.0.0", port=8767):
    """启动TCP服务器"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
        server.listen(5)
        print(f"TCP服务器启动: {host}:{port}")
        print("按 Ctrl+C 停止服务器")

        while True:
            client, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client, addr))
            thread.daemon = True
            thread.start()

    except KeyboardInterrupt:
        print("\n服务器停止")
    except Exception as e:
        print(f"服务器错误: {e}")
    finally:
        server.close()

def test_connection(port=8767):
    """测试连接"""
    print(f"\n测试连接: 192.168.0.127:{port}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        result = sock.connect_ex(('192.168.0.127', port))
        if result == 0:
            print("✅ 连接成功")

            # 发送测试数据
            sock.send(b"GET / HTTP/1.1\r\n\r\n")

            # 接收响应
            try:
                response = sock.recv(1024)
                print(f"服务器响应: {response[:100]}")
            except socket.timeout:
                print("⚠️  服务器无响应")

            sock.close()
            return True
        else:
            print(f"❌ 连接失败 (错误码: {result})")
            return False
    except Exception as e:
        print(f"❌ 测试错误: {e}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    print("=" * 50)
    print("简单TCP服务器测试")
    print("=" * 50)

    # 先测试端口
    print("\n1. 测试端口8767...")
    if test_connection(8767):
        print("端口已被占用")
    else:
        print("端口可用")

    # 启动服务器
    print("\n2. 启动TCP服务器...")
    print("手机可以连接: 192.168.0.127:8767")
    print("或使用浏览器访问: http://192.168.0.127:8767")

    start_tcp_server(port=8767)