#!/usr/bin/env python3
"""
最简单的WebSocket测试
"""

import asyncio
import websockets

async def test():
    uri = "ws://192.168.0.127:8765"

    print(f"Testing connection to: {uri}")

    try:
        async with websockets.connect(uri) as ws:
            print("SUCCESS: Connected to WebSocket server!")

            # Try to receive welcome message
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=3)
                print(f"Received: {msg}")
            except asyncio.TimeoutError:
                print("No message received (might be normal)")

            # Send a test command
            await ws.send('{"command": "status"}')

            try:
                resp = await asyncio.wait_for(ws.recv(), timeout=3)
                print(f"Response: {resp}")
            except asyncio.TimeoutError:
                print("No response received")

            return True

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"ERROR: Invalid HTTP status: {e}")
        return False
    except websockets.exceptions.InvalidHandshake as e:
        print(f"ERROR: Handshake failed: {e}")
        return False
    except ConnectionRefusedError:
        print("ERROR: Connection refused")
        return False
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("WebSocket Connection Test")
    print("=" * 50)

    result = asyncio.run(test())

    if result:
        print("\nSUCCESS: WebSocket server is working!")
        print("Phone should be able to connect.")
        print("Use: 192.168.0.127:8765 in phone app")
    else:
        print("\nFAILED: Cannot connect to WebSocket server")
        print("\nPossible issues:")
        print("1. Server not running (run 'python main.py')")
        print("2. Firewall blocking port 8765")
        print("3. Server not started (click 'Start WebSocket Server' button)")
        print("4. Network issue")

    print("\n" + "=" * 50)