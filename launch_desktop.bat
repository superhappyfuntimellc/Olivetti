@echo off
REM Olivetti Desktop Launcher for Windows

echo ========================================
echo   Olivetti Creative Editing Partner
echo          Desktop Mode
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
)

REM Ask about desktop mode
echo Desktop Mode Options:
echo 1. Native desktop window (requires pywebview)
echo 2. Browser window (default)
echo.
set /p mode="Choose mode (1 or 2, default=2): "

if "%mode%"=="1" (
    python -c "import webview" >nul 2>&1
    if errorlevel 1 (
        echo Installing pywebview for native desktop window...
        python -m pip install pywebview>=4.0.0
    )
)

REM Launch desktop mode
echo.
echo Launching Olivetti...
python desktop_launcher.py

pause
