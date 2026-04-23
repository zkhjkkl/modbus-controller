@echo off
echo ========================================
echo Modbus HTTP Gateway - EXE Build Script
echo ========================================
echo.
echo This script will build ModbusHTTPGateway.exe
echo.
echo Press any key to start, or Ctrl+C to cancel...
pause >nul
echo.

echo Step 1: Checking Python...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please run: python --version
    echo If that fails, try: py --version
    echo.
    echo Make sure Python 3.6+ is installed and in PATH.
    pause
    exit /b 1
)
python --version

echo.
echo Step 2: Checking PyInstaller...
python -m pip show PyInstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller!
        echo Please run manually: python -m pip install pyinstaller
        pause
        exit /b 1
    )
    echo PyInstaller installed.
) else (
    echo PyInstaller already installed.
)

echo.
echo Step 3: Installing dependencies...
python -m pip install -r requirements-http.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Please run manually: python -m pip install -r requirements-http.txt
    pause
    exit /b 1
)
echo Dependencies installed.

echo.
echo Step 4: Creating build directories...
if not exist "build" mkdir build
if not exist "dist" mkdir dist

echo.
echo Step 5: Building EXE file...
echo This may take a few minutes, please wait...
echo.

python -m PyInstaller --onefile ^
    --name "ModbusHTTPGateway" ^
    --add-data "templates;templates" ^
    --add-data "config.json;." ^
    --clean ^
    app.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo EXE file: dist\ModbusHTTPGateway.exe
echo.
echo To use:
echo 1. Copy ModbusHTTPGateway.exe to target computer
echo 2. Double-click ModbusHTTPGateway.exe
echo 3. Computer: http://localhost:5000
echo 4. Mobile/tablet: http://<computer-ip>:5000
echo.
echo Note: First run may require firewall access for port 5000
echo ========================================
echo.
pause