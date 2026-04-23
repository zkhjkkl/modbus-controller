@echo off
echo Python PATH Fix Tool
echo ====================
echo.

set PYTHON_DIR=C:\Users\BRT252\AppData\Local\Programs\Python\Python314
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set SCRIPTS_DIR=%PYTHON_DIR%\Scripts

echo Checking Python installation...
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python not found at: %PYTHON_DIR%
    echo.
    echo Please check if Python 3.14.4 is installed elsewhere.
    pause
    exit /b 1
)

echo OK: Python found at %PYTHON_DIR%
echo.

echo Current PATH status:
echo.
python --version 2>nul
if %errorlevel% equ 0 (
    echo ✓ 'python' command works from PATH
) else (
    echo ✗ 'python' command NOT in PATH
)

py --version 2>nul
if %errorlevel% equ 0 (
    echo ✓ 'py' command works from PATH
) else (
    echo ✗ 'py' command NOT in PATH
)

echo.
echo ====================================================
echo OPTION 1: Use full path (no PATH changes needed)
echo ====================================================
echo You can use the full path to Python:
echo   "%PYTHON_EXE%" main.py
echo.
echo We've created a run script for you:
echo   run_with_full_path.bat
echo.
(
echo @echo off
echo echo Running Modbus Gateway with full Python path...
echo "%PYTHON_EXE%" main.py
echo pause
) > run_with_full_path.bat

echo ====================================================
echo OPTION 2: Add Python to PATH (recommended)
echo ====================================================
echo.
echo To add Python to PATH permanently:
echo.
echo METHOD A: Manual (for all users, needs Admin)
echo   1. Press Win+R, type: sysdm.cpl
echo   2. Click "Advanced" tab
echo   3. Click "Environment Variables"
echo   4. Under "System variables", find "Path"
echo   5. Click "Edit"
echo   6. Add these two entries:
echo        %PYTHON_DIR%
echo        %SCRIPTS_DIR%
echo   7. Click OK, OK, OK
echo   8. Restart terminal
echo.
echo METHOD B: Using PowerShell (Admin)
echo   Run PowerShell as Administrator and execute:
echo   [Environment]::SetEnvironmentVariable("Path", `
echo     [Environment]::GetEnvironmentVariable("Path", "User") + `
echo     ";%PYTHON_DIR%;%SCRIPTS_DIR%", "User")
echo   Then restart terminal.
echo.
echo METHOD C: Temporary (current terminal only)
echo   Run this command:
echo   set PATH=%PYTHON_DIR%;%SCRIPTS_DIR%;%PATH%
echo   Then test: python --version
echo.

echo ====================================================
echo QUICK FIX: Try to add to PATH now (Admin required)
echo ====================================================
echo.
echo Do you want to try adding Python to PATH now?
echo This requires Administrator privileges.
echo.
set /p choice="Add to PATH? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo Attempting to add Python to PATH...

    REM Try to add to user PATH
    setx PATH "%PATH%;%PYTHON_DIR%;%SCRIPTS_DIR%" >nul 2>nul
    if %errorlevel% equ 0 (
        echo ✓ Added to PATH (user)
    ) else (
        echo ✗ Failed to add to PATH (may need Admin)
        echo.
        echo Try running this script as Administrator:
        echo   1. Right-click this file
        echo   2. Select "Run as administrator"
    )
)

echo.
echo ====================================================
echo NEXT STEPS
echo ====================================================
echo.
echo 1. To install dependencies, run:
echo    install_with_full_path.bat
echo.
echo 2. To run gateway, use:
echo    - run_with_full_path.bat (no PATH changes)
echo    - OR fix PATH first, then use: python main.py
echo.
echo 3. After fixing PATH, test with:
echo    python --version
echo.
pause