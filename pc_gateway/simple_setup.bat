@echo off
echo Modbus Gateway Simple Setup
echo.

REM Find Python
set PYTHON=
python --version >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON=python
    goto found_python
)

py --version >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON=py
    goto found_python
)

REM Check for Python 3.14.4
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" (
    set PYTHON="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe"
    goto found_python
)

if exist "C:\Program Files\Python314\python.exe" (
    set PYTHON="C:\Program Files\Python314\python.exe"
    goto found_python
)

echo ERROR: Python not found!
echo.
echo If you installed Python 3.14.4, try:
echo   1. Restart your computer
echo   2. Or use full path to run:
echo      "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" main.py
echo.
pause
exit /b 1

:found_python
echo Using Python: %PYTHON%
%PYTHON% --version
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
echo.

%PYTHON% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Trying with mirror source...
    %PYTHON% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install dependencies.
        echo Try: %PYTHON% -m pip install PyQt6 pymodbus websockets
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Dependencies installed!
echo.

REM Create run script
echo Creating run script...
(
echo @echo off
echo echo Starting Modbus Gateway...
echo %PYTHON% main.py
echo pause
) > run.bat

echo Run script: run.bat
echo.
echo To start gateway: run.bat
echo Or: %PYTHON% main.py
echo.
echo For tablet connection:
echo   1. Find PC IP: ipconfig
echo   2. In tablet: IP:8765
echo   3. Example: 192.168.1.100:8765
echo.
pause