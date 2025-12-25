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
@server.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        target = request.form.get('target')

        # 1. Sanitize (Python Side)
        # Example: Block specific sensitive words
        if "secret" in prompt.lower() or "password" in prompt.lower():
            return "<h1 style='color:red; font-family:sans-serif; text-align:center; margin-top:50px;'>🚫 Prompt Blocked: Sensitive Content Detected</h1><div style='text-align:center'><a href='/'>Go Back</a></div>"

        # 2. Seamless Handoff
        pyperclip.copy(prompt)
        webbrowser.open(target) # Opens external AI in default browser

        # 3. Auto-Paste (Background Thread)
        def inject_prompt():
            time.sleep(1.5) # Wait for browser to open and focus
            pyautogui.hotkey('ctrl', 'v')
        
        threading.Thread(target=inject_prompt).start()
        
        return redirect('/')

    return """
    <!DOCTYPE html>
    <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #f0f2f5;">
        <h1>Airlock Secure Workspace</h1>
        <p>Type your prompt here. We will sanitize it and paste it into the AI for you.</p>
        <form method="POST">
            <textarea name="prompt" rows="5" style="width: 80%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;" placeholder="Enter safe prompt..."></textarea>
            <br><br>
            <button type="submit" name="target" value="https://gemini.google.com" style="padding:15px 30px; background:#4285F4; color:white; border:none; border-radius:6px; cursor:pointer;">
                Sanitize & Launch Gemini
            </button>
            <button type="submit" name="target" value="https://chatgpt.com" style="padding:15px 30px; background:#10a37f; color:white; border:none; border-radius:6px; cursor:pointer;">
                Sanitize & Launch ChatGPT
            </button>
        </form>
    </body>
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