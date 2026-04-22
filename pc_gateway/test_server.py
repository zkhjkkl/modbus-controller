#!/usr/bin/env python3
"""
简单服务器测试 - 无Unicode字符
"""

import socket
import sys

def test_port(port):
    """测试端口"""
    print(f"Testing port {port}...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        result = sock.connect_ex(('192.168.0.127', port))
        if result == 0:
            print(f"Port {port} is OPEN")
            sock.close()
            return True
        else:
            print(f"Port {port} is CLOSED (error: {result})")
            sock.close()
            return False
    except Exception as e:
        print(f"Error testing port {port}: {e}")
        return False

def start_simple_server(port=8767):
    """启动简单服务器"""
    print(f"\nStarting TCP server on port {port}...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind(('0.0.0.0', port))
        server.listen(5)
        print(f"Server started: 192.168.0.127:{port}")
        print("Press Ctrl+C to stop")

        while True:
            client, addr = server.accept()
            print(f"Client connected: {addr}")

            # 简单响应
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nServer is working!"
            client.send(response)
            client.close()

    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Server Test")
    print("=" * 50)

    # 测试常用端口
    ports = [8766, 8765, 8767, 8080, 8888]

    for port in ports:
        test_port(port)

    print("\n" + "=" * 50)
    print("Starting test server on port 8767...")
    print("Phone can test with: 192.168.0.127:8767")
    print("=" * 50)

    start_simple_server(8767)