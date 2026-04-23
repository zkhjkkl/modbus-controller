#!/usr/bin/env python3
"""
测试PyQt6/PyQt5是否正常工作
"""

import sys

print("Testing Qt imports...")

# 先测试PyQt6
try:
    print("\n1. Testing PyQt6...")
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QApplication
    print("   ✓ PyQt6 imports successful")
    print("   PyQt6 version:", Qt.PYQT_VERSION_STR if hasattr(Qt, 'PYQT_VERSION_STR') else "Unknown")
except ImportError as e:
    print(f"   ✗ PyQt6 import failed: {e}")
except Exception as e:
    print(f"   ✗ PyQt6 DLL error: {e}")

# 测试PyQt5
try:
    print("\n2. Testing PyQt5...")
    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.QtWidgets import QApplication
    print("   ✓ PyQt5 imports successful")
    print("   PyQt5 version:", QT_VERSION_STR)
except ImportError as e:
    print(f"   ✗ PyQt5 not installed: {e}")
except Exception as e:
    print(f"   ✗ PyQt5 error: {e}")

# 测试PySide6
try:
    print("\n3. Testing PySide6...")
    from PySide6.QtCore import __version__
    from PySide6.QtWidgets import QApplication
    print("   ✓ PySide6 imports successful")
    print("   PySide6 version:", __version__)
except ImportError as e:
    print(f"   ✗ PySide6 not installed: {e}")
except Exception as e:
    print(f"   ✗ PySide6 error: {e}")

print("\n" + "="*50)
print("SUMMARY:")
print("="*50)

print("\nIf PyQt6 fails with 'DLL load failed', you need to:")
print("1. Install Microsoft Visual C++ Redistributable")
print("   Download: https://aka.ms/vs/17/release/vc_redist.x64.exe")
print("2. Or use PyQt5 instead (more stable on Windows)")

print("\nTo install PyQt5:")
print("   pip install PyQt5")

print("\nTo install PySide6:")
print("   pip install PySide6")