@echo off
echo Fixing Qt DLL issues...
echo.

echo 1. Testing Qt imports...
python test_qt.py
echo.

echo 2. Installing Visual C++ Redistributable is recommended.
echo    Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
echo    Install and restart computer.
echo.

echo 3. Option A: Reinstall PyQt6
echo    pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y
echo    pip install PyQt6==6.6.0 --force-reinstall
echo.

echo 4. Option B: Switch to PyQt5 (recommended for Windows)
echo    a. Edit requirements.txt: change PyQt6==6.6.0 to PyQt5==5.15.10
echo    b. Run: pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y
echo    c. Run: pip install -r requirements.txt
echo    d. Update main.py imports from PyQt6 to PyQt5
echo.

echo 5. Option C: Switch to PySide6
echo    a. Edit requirements.txt: change PyQt6==6.6.0 to PySide6==6.6.0
echo    b. Run: pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y
echo    c. Run: pip install -r requirements.txt
echo    d. Update main.py imports from PyQt6 to PySide6
echo.

echo After fixing, test with: python main.py
pause