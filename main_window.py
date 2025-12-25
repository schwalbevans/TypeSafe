import sys
import os
import threading
import webbrowser
import time
import subprocess
import shutil
import pyperclip # pip install pyperclip
import pyautogui # pip install pyautogui
from flask import Flask, jsonify, request, redirect # pip install flask

# --- 1. THE INTERNAL SERVER (Backend) ---
server = Flask(__name__)
global_window = None


# A. serve the Launcher HTML securely
@server.route('/')
def allthetime():
    return """
    
    """

def start_server():
    # Run quietly in background
    server.run(port=5000, use_reloader=False)

# --- 4. MAIN APP ---
if __name__ == "__main__":

    # 2. Launch in App Mode (Chrome/Chromium)
    url = "http://127.0.0.1:5000"
    print("[AIRLOCK] Launching in App Mode...")
    
    # Find a browser that supports --app (Chrome/Chromium based)
    browser_cmd = None

    # 1. Try specific Windows paths first (since they aren't usually in PATH)
    if sys.platform == "win32":
        win_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        for path in win_paths:
            if os.path.exists(path):
                browser_cmd = path
                break

    # 2. Fallback to PATH (Linux/Mac or custom Windows setup)
    if not browser_cmd:
        chromium_browsers = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "brave-browser", "microsoft-edge", "microsoft-edge-stable", "chrome", "msedge"]
        for browser in chromium_browsers:
            if shutil.which(browser):
                browser_cmd = shutil.which(browser)
                break
            
    if browser_cmd:
        print(f"[AIRLOCK] Found browser: {browser_cmd}")
        subprocess.Popen([browser_cmd, f"--app={url}"])
    elif shutil.which("firefox"):
        # Firefox doesn't support --app, but --new-window separates it
        subprocess.Popen(["firefox", "--new-window", url])   
    else:
        # Fallback if no suitable browser found
        webbrowser.open(url)    
    
    # 3. Run Server (Blocking)
    start_server()