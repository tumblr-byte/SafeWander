@echo off
REM SafeWonder - Quick Run Script for Windows
REM This script runs the SafeWonder app locally

echo ========================================
echo    SafeWonder - Travel Safety Assistant
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/3] Checking Python packages...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Streamlit not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [2/3] Checking environment setup...
if not exist ".env" (
    if not exist ".streamlit\secrets.toml" (
        echo.
        echo WARNING: No .env or secrets.toml found
        echo Please create .env with your GROQ_API_KEY
        echo.
        echo Example:
        echo GROQ_API_KEY=your_key_here
        echo.
        pause
    )
)

echo [3/3] Starting SafeWonder...
echo.
echo Opening app in your browser...
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

pause
