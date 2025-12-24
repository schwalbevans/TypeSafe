import sys
import os
import threading
import webview # pip install pywebview
from flask import Flask, jsonify, request # pip install flask

# --- 0. LINUX CLEANUP ---
if sys.platform.startswith("linux"):
    if "LD_LIBRARY_PATH" in os.environ: del os.environ["LD_LIBRARY_PATH"]
    if "GTK_PATH" in os.environ: del os.environ["GTK_PATH"]
    os.environ["GDK_BACKEND"] = "x11"

# --- 1. THE INTERNAL SERVER (Backend) ---
server = Flask(__name__)


# A. serve the Launcher HTML securely
@server.route('/')
def home():
    return """
    <!DOCTYPE html>
    <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #f0f2f5;">
        <h1>Airlock Secure Workspace</h1>
        <p>Select your secure environment:</p>
        <a href="https://gemini.google.com" 
           style="display:inline-block; padding:15px 30px; margin:10px; background:#4285F4; color:white; border-radius:6px; font-size:16px; text-decoration:none;">
            Launch Google Gemini
        </a>
        <a href="https://chatgpt.com" 
           style="display:inline-block; padding:15px 30px; margin:10px; background:#10a37f; color:white; border-radius:6px; font-size:16px; text-decoration:none;">
            Launch OpenAI ChatGPT
        </a>
    </body>
    """

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

# --- 2. THE GUARD SCRIPT (Frontend) ---
GUARD_JS = """
console.log("🛡️ Airlock Active");

// Inject "Back to Home" Button
var homeBtn = document.createElement("button");
homeBtn.innerHTML = "🏠 Home";
homeBtn.style.cssText = "position:fixed; bottom:20px; right:20px; z-index:2147483647; padding:10px 20px; background:#333; color:white; border:none; border-radius:5px; cursor:pointer; font-family:sans-serif; font-size:14px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);";
homeBtn.onclick = function() { window.location.href = 'http://127.0.0.1:5000'; };
document.body.appendChild(homeBtn);

document.addEventListener('keydown', function(e) {
    let target = e.target;
    // Detect typing in input fields
    if ((target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) && e.key === 'Enter' && !e.shiftKey) {
        let text = target.value || target.innerText;
        
        // Send HTTP Request to our local Flask server
        fetch('http://127.0.0.1:5000/scan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'blocked') {
                e.preventDefault();
                e.stopPropagation();
                alert("🛑 BLOCKED BY AIRLOCK:\\n" + data.reason);
            }
        });
    }
}, true);
"""

# --- 3. EVENT LISTENER ---
def on_page_loaded(window):
    # Only inject security when we are NOT on the launcher
    url = window.get_current_url()
    if "127.0.0.1" not in url:
        # We are on Google/ChatGPT -> Inject Guard
        window.evaluate_js(GUARD_JS)

# --- 4. MAIN APP ---
if __name__ == "__main__":
    # 1. Start Background Server
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # 2. Start Window (Loading the URL, not raw HTML)
    window = webview.create_window(
        title="Airlock Secure Workspace",
        url="http://127.0.0.1:5000", # <--- Safe URL load
        width=1200, 
        height=800
    )
    
    # 3. Attach Event
    window.events.loaded += on_page_loaded
    
    # 4. Launch
    webview.start(debug=True)