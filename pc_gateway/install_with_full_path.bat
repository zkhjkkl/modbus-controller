@echo off
echo Modbus Gateway Installation (using full Python path)
echo ====================================================
echo.

set PYTHON_PATH=C:\Users\BRT252\AppData\Local\Programs\Python\Python314\python.exe

echo Checking Python at: %PYTHON_PATH%
if not exist "%PYTHON_PATH%" (
    echo ERROR: Python not found at expected location!
    echo.
    echo Please check if Python 3.14.4 is installed at:
    echo   %PYTHON_PATH%
    echo.
    echo If installed elsewhere, update this script with correct path.
    pause
    exit /b 1
)

echo OK: Python found
"%PYTHON_PATH%" --version
echo.

echo Installing dependencies...
echo This may take a few minutes...
echo.

"%PYTHON_PATH%" -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Trying with mirror source...
    "%PYTHON_PATH%" -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install dependencies.
        echo Try manually: "%PYTHON_PATH%" -m pip install PyQt6 pymodbus websockets
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Dependencies installed successfully!
echo.

echo Creating run script...
(
echo @echo off
echo echo Starting Modbus Gateway...
echo "%PYTHON_PATH%" main.py
echo pause
) > run_gateway.bat

echo Run script created: run_gateway.bat
echo.

echo ====================================================
echo INSTALLATION COMPLETE!
echo ====================================================
echo.
echo To start the gateway:
echo   1. Double-click run_gateway.bat
echo   OR
echo   2. Run: "%PYTHON_PATH%" main.py
echo.
echo IMPORTANT: For tablet connection:
echo   1. Find your PC IP address (run: ipconfig)
echo   2. In tablet app, set server to: YOUR_IP:8765
echo   3. Example: 192.168.1.100:8765
echo.
pause