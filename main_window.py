import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot, QUrl, pyqtSignal

# --- THE BRIDGE ---
# This class handles communication between JavaScript and Python
class Bridge(QObject):
    # Signal to send data FROM Python TO JavaScript
    sendToJs = pyqtSignal(str)

    @pyqtSlot(str)
    def receiveFromJs(self, message_json):
        """
        Triggered when JavaScript calls backend.receiveFromJs()
        """
        data = json.loads(message_json)
        user_text = data.get("text", "")
        print(f"Python received: {user_text}")

        # --- YOUR LOGIC GOES HERE ---
        # 1. Run PII Checks
        
        # 2. Call OpenAI (if safe)
        # 3. Send response back to UI
        
        # For this skeleton, we just echo it back after a delay
        response = {
            "role": "assistant", 
            "content": f"I received your message: '{user_text}'. <br><b>Python Logic is working!</b>"
        }
        self.sendToJs.emit(json.dumps(response))

# --- MAIN WINDOW ---
class AirlockWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Airlock - Secure Chat")
        self.resize(1000, 800)

        # 1. Setup Web Engine
        self.browser = QWebEngineView()
        
        # 2. Setup Web Channel (The Bridge)
        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.channel.registerObject('backend', self.bridge)
        self.browser.page().setWebChannel(self.channel)

        # 3. Load HTML File
        # We need the absolute path to index.html for PyQt to load it correctly
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "index.html")
        self.browser.setUrl(QUrl.fromLocalFile(html_path))

        # 4. Layout
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.setContentsMargins(0, 0, 0, 0) # No borders, full screen web view
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AirlockWindow()
    window.show()
    sys.exit(app.exec())