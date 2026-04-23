@echo off
echo Testing Python installation...
echo.

echo 1. Testing 'python' command:
python --version 2>nul
if %errorlevel% equ 0 (
    echo   OK: python command works
) else (
    echo   FAIL: python command not found
)

echo.
echo 2. Testing 'py' command:
py --version 2>nul
if %errorlevel% equ 0 (
    echo   OK: py command works
) else (
    echo   FAIL: py command not found
)

echo.
echo 3. Checking common Python locations:
set found=0

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" (
    echo   Found: C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\
    set found=1
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo   Found: C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\
    set found=1
)

if exist "C:\Program Files\Python314\python.exe" (
    echo   Found: C:\Program Files\Python314\
    set found=1
)

if exist "C:\Program Files\Python311\python.exe" (
    echo   Found: C:\Program Files\Python311\
    set found=1
)

if %found% equ 0 (
    echo   No Python found in common locations
)

echo.
echo 4. Testing with full path (if Python 3.14.4 installed):
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" (
    echo   Testing full path...
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" --version
    if %errorlevel% equ 0 (
        echo   OK: Python 3.14.4 works with full path
    )
)

echo.
echo ========================================
echo SUMMARY:
echo.

if %found% equ 1 (
    echo Python is installed but may not be in PATH.
    echo.
    echo To run the gateway, use full path:
    echo   "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" main.py
    echo.
    echo Or add Python to PATH:
    echo   1. Search for "Environment Variables"
    echo   2. Edit "Path" variable
    echo   3. Add Python installation folder
    echo   4. Add Python\Scripts folder
) else (
    echo Python not found.
    echo.
    echo If you installed Python 3.14.4, check:
    echo   1. Installation location
    echo   2. If "Add to PATH" was checked during install
    echo   3. Try restarting your computer
)

echo.
pause