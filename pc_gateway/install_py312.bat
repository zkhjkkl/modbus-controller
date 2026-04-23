@echo off
echo Installing dependencies for Python 3.12.0...
echo.

"C:\Users\BRT252\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Trying with mirror source...
    "C:\Users\BRT252\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install dependencies.
        echo Try manually: "C:\Users\BRT252\AppData\Local\Programs\Python\Python312\python.exe" -m pip install PyQt6 pymodbus websockets
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
echo echo Starting Modbus Gateway with Python 3.12.0...
echo "C:\Users\BRT252\AppData\Local\Programs\Python\Python312\python.exe" main.py
echo pause
) > run_py312.bat

echo Run script created: run_py312.bat
echo.
echo To start gateway, double-click run_py312.bat
echo Or run: "C:\Users\BRT252\AppData\Local\Programs\Python\Python312\python.exe" main.py
echo.
pause