@echo off
echo Testing Python environment...
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    echo python.exe found.
    python --version
) else (
    echo python.exe not found.
)

echo.
where py >nul 2>nul
if %errorlevel% equ 0 (
    echo py.exe found.
    py --version
) else (
    echo py.exe not found.
)

echo.
echo Press any key to exit...
pause >nul