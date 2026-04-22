#!/usr/bin/env python3
"""
模拟手机连接测试
测试WebSocket服务器是否正常工作
"""

import asyncio
import websockets
import sys

async def test_connection(host="192.168.0.127", port=8766):
    """模拟手机连接"""
    uri = f"ws://{host}:{port}"

    print(f"模拟手机连接: {uri}")
    print("=" * 50)

    try:
        # 连接服务器
        print("1. 建立WebSocket连接...")
        websocket = await websockets.connect(uri)
        print("   ✅ 连接建立成功")

        # 接收欢迎消息
        print("\n2. 接收服务器消息...")
        try:
            welcome = await asyncio.wait_for(websocket.recv(), timeout=3)
            print(f"   ✅ 收到消息: {welcome}")
        except asyncio.TimeoutError:
            print("   ⚠️  没有收到欢迎消息（可能正常）")

        # 发送测试消息
        print("\n3. 发送测试消息...")
        test_msg = '{"test": "hello"}'
        await websocket.send(test_msg)
        print(f"   ✅ 已发送: {test_msg}")

        # 接收回显
        print("\n4. 等待服务器响应...")
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=3)
            print(f"   ✅ 收到响应: {response}")
        except asyncio.TimeoutError:
            print("   ⚠️  没有收到响应")

        # 关闭连接
        print("\n5. 关闭连接...")
        await websocket.close()
        print("   ✅ 连接已关闭")

        return True

    except websockets.exceptions.InvalidHandshake as e:
        print(f"❌ 握手失败: {e}")
        print("可能原因: 服务器不是WebSocket服务器")
        return False
    except ConnectionRefusedError:
        print("❌ 连接被拒绝")
        print("可能原因:")
        print("  - 服务器未运行")
        print("  - 防火墙阻止")
        print("  - 端口错误")
        return False
    except asyncio.TimeoutError:
        print("❌ 连接超时")
        print("可能原因: 网络延迟或服务器无响应")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {type(e).__name__}: {e}")
        return False

async def test_multiple_ports():
    """测试多个端口"""
    ports = [8766, 8765, 8080, 8888]

    for port in ports:
        print(f"\n{'='*60}")
        print(f"测试端口: {port}")
        print('='*60)

        success = await test_connection(port=port)

        if success:
            print(f"\n✅ 端口 {port} 工作正常!")
            break
        else:
            print(f"\n❌ 端口 {port} 测试失败")

async def main():
    print("手机连接模拟测试")
    print("=" * 60)

    # 先测试8766端口（echo服务器）
    print("测试1: Echo服务器 (端口8766)")
    success1 = await test_connection(port=8766)

    if success1:
        print("\n" + "="*60)
        print("✅ Echo服务器工作正常!")
        print("手机应该能连接到: 192.168.0.127:8766")
        print("\n问题可能在:")
        print("1. 手机App代码")
        print("2. 手机网络设置")
        print("3. 路由器AP隔离")
    else:
        print("\n" + "="*60)
        print("❌ Echo服务器测试失败")
        print("\n可能原因:")
        print("1. 服务器未运行 (运行 'python simple_echo_server.py')")
        print("2. 防火墙阻止端口8766")
        print("3. IP地址错误")

    print("\n" + "="*60)
    print("测试完成")

if __name__ == "__main__":
    asyncio.run(main())