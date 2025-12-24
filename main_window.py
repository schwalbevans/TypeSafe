import sys
import os
import threading
import webbrowser
import subprocess
import shutil
from flask import Flask, jsonify, request, redirect # pip install flask
from pynput import keyboard # pip install pynput


# --- 1. THE INTERNAL SERVER (Backend) ---
server = Flask(__name__)
global_window = None


# A. serve the Launcher HTML securely
@server.route('/')
def home():
    return """
    <!DOCTYPE html>
    <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #f0f2f5;">
        <h1>Airlock Secure Workspace</h1>
        <p>Select your secure environment:</p>
        <button onclick="window.location.href='https://gemini.google.com'" 
           style="display:inline-block; padding:15px 30px; margin:10px; background:#4285F4; color:white; border-radius:6px; font-size:16px; border:none; cursor:pointer;">
            Launch Google Gemini
        </button>
        <button onclick="window.location.href='https://chatgpt.com'" 
           style="display:inline-block; padding:15px 30px; margin:10px; background:#10a37f; color:white; border-radius:6px; font-size:16px; border:none; cursor:pointer;">
            Launch OpenAI ChatGPT
        </button>
    </body>
    """

# C. Handle Navigation (Bypassing JS Bridge)
@server.route('/navigate')
def navigate():
    url = request.args.get('url')
    return redirect(url)

# B. Handle Security Checks (The "Bridge")
@server.route('/scan', methods=['POST'])
def scan_text():
    data = request.json
    text = data.get('text', '')
    print(f"[AIRLOCK] 🕵️ Scanning: {text[:30]}...")
    
    if "sk-" in text:
        return jsonify({"status": "blocked", "reason": "API Key detected"})
    elif "confidential" in text.lower():
        return jsonify({"status": "blocked", "reason": "Confidential marker"})
    
    return jsonify({"status": "safe"})

def start_server():
    # Run quietly in background
    server.run(port=5000, use_reloader=False)

# --- 2. PYTHON KEYBOARD MONITOR (No JS Injection) ---
keystroke_buffer = []
is_window_focused = True

def on_focus():
    global is_window_focused
    is_window_focused = True

def on_blur():
    global is_window_focused
    is_window_focused = False

def on_press(key):
    global keystroke_buffer, is_window_focused
    if not is_window_focused: return
    try:
        # Add character to buffer
        if hasattr(key, 'char') and key.char:
            keystroke_buffer.append(key.char)
    except AttributeError:
        pass

    # Check buffer for keywords
    current_text = "".join(keystroke_buffer[-20:]) # Keep last 20 chars
    if "confidential" in current_text.lower():
        print("\n[AIRLOCK] 🚨 SECURITY ALERT: 'Confidential' typed! (Detected via Python)")
        keystroke_buffer = [] # Reset buffer

# --- 4. MAIN APP ---
if __name__ == "__main__":
    # 1. Start Keyboard Listener (Non-blocking)
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # 2. Launch in App Mode (Chrome/Chromium)
    url = "http://127.0.0.1:5000"
    print("[AIRLOCK] Launching in App Mode...")
    
    # Find a browser that supports --app (Chrome/Chromium based)
    browser_cmd = None
    chromium_browsers = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "brave-browser", "microsoft-edge", "microsoft-edge-stable"]
    for browser in chromium_browsers:
        if shutil.which(browser):
            browser_cmd = browser
            break
            
    if browser_cmd:
        subprocess.Popen([browser_cmd, f"--app={url}"])
    elif shutil.which("firefox"):
        # Firefox doesn't support --app, but --new-window separates it
        subprocess.Popen(["firefox", "--new-window", url])
    else:
        # Fallback if no suitable browser found
        webbrowser.open(url)
    
    # 3. Run Server (Blocking)
    start_server()