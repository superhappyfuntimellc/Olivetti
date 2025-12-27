#!/bin/bash
# Olivetti Desktop Launcher for Unix/Linux/macOS

echo "🖥️  Olivetti Creative Editing Partner - Desktop Mode"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 Installing dependencies..."
    python3 -m pip install -r requirements.txt
fi

# Ask if user wants desktop window mode
echo "Desktop Mode Options:"
echo "1. Native desktop window (requires pywebview)"
echo "2. Browser window (default)"
echo ""
read -p "Choose mode (1 or 2, default=2): " mode

if [ "$mode" = "1" ]; then
    # Check if pywebview is installed
    if ! python3 -c "import webview" &> /dev/null; then
        echo "📦 Installing pywebview for native desktop window..."
        python3 -m pip install pywebview>=4.0.0
    fi
fi

# Launch desktop mode
echo ""
echo "🚀 Launching Olivetti..."
python3 desktop_launcher.py
