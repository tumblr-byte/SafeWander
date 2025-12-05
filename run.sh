#!/bin/bash
# SafeWonder - Quick Run Script for Mac/Linux
# This script runs the SafeWonder app locally

echo "========================================"
echo "  SafeWonder - Travel Safety Assistant"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/3] Checking Python packages..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo ""
    echo "Streamlit not found. Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo "[2/3] Checking environment setup..."
if [ ! -f ".env" ] && [ ! -f ".streamlit/secrets.toml" ]; then
    echo ""
    echo "WARNING: No .env or secrets.toml found"
    echo "Please create .env with your GROQ_API_KEY"
    echo ""
    echo "Example:"
    echo "GROQ_API_KEY=your_key_here"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

echo "[3/3] Starting SafeWonder..."
echo ""
echo "Opening app in your browser..."
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
