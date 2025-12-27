#!/usr/bin/env python3
"""
Desktop launcher for Olivetti Creative Editing Partner
Runs the Streamlit app in a desktop window using webview
"""

import os
import sys
import subprocess
import threading
import time
import socket
import webbrowser
from pathlib import Path

# Optional webview import for true desktop experience
try:
    import webview
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False


def find_free_port():
    """Find a free port for Streamlit to use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def run_streamlit(port):
    """Run Streamlit server on specified port."""
    app_dir = Path(__file__).parent
    app_file = app_dir / "app.py"
    
    # Run streamlit with custom port and hide some UI elements for desktop feel
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_file),
        "--server.port", str(port),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--server.fileWatcherType", "none"
    ]
    
    subprocess.run(cmd)


def launch_desktop_mode():
    """Launch Olivetti in desktop mode."""
    print("🖥️  Launching Olivetti Creative Editing Partner (Desktop Mode)")
    print("=" * 60)
    
    # Find free port
    port = find_free_port()
    url = f"http://localhost:{port}"
    
    print(f"Starting server on port {port}...")
    
    # Start Streamlit in a background thread
    server_thread = threading.Thread(target=run_streamlit, args=(port,), daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Check if webview is available
    if HAS_WEBVIEW:
        print("Opening desktop window with webview...")
        print("=" * 60)
        # Create a desktop window with webview
        webview.create_window(
            '✍️ Olivetti Creative Editing Partner',
            url,
            width=1400,
            height=900,
            resizable=True,
            fullscreen=False,
            min_size=(1000, 700)
        )
        webview.start()
    else:
        print("Opening in default browser...")
        print("(Install 'pywebview' for a true desktop window experience)")
        print("=" * 60)
        webbrowser.open(url)
        
        # Keep the script running
        try:
            server_thread.join()
        except KeyboardInterrupt:
            print("\n\nShutting down Olivetti...")
            sys.exit(0)


if __name__ == "__main__":
    launch_desktop_mode()
