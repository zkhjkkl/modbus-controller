@echo off
echo Testing Python environment...
echo.

echo Checking for python.exe...
where python 2>nul
if %errorlevel% equ 0 (
    echo python.exe found.
    python --version
) else (
    echo python.exe not found.
)

echo.
echo Checking for py.exe...
where py 2>nul
if %errorlevel% equ 0 (
    echo py.exe found.
    py --version
) else (
    echo py.exe not found.
)

echo.
echo Checking PATH environment variable...
echo %PATH%

echo.
pause