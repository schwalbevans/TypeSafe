import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, QFile, QIODevice, Qt


# --- THE BRIDGE (Python <-> JS) ---
class SecurityBridge(QObject):
    @pyqtSlot(str)
    def check_text(self, text):
        """Called from JS when user hits Enter"""
        # This PRINT statement is what you should see in your terminal
        print(f"\n[PYTHON] 🔒 Intercepted Message: {text}")
        
        # --- PII DETECTION LOGIC ---
        # Simple example: Block if it contains "sk-" (API Key format)
        if "sk-" in text:
            print("[PYTHON] ❌ BLOCKING: API Key detected!")
            # In a real app, you would signal JS to stop the submit here
        else:
            print("[PYTHON] ✅ SAFE: content looks okay.")

# --- THE BROWSER WINDOW ---
class AirlockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Airlock AI Wrapper")
        self.resize(1200, 800)
        
        self.sidebar_dock = QDockWidget("Select your AI", self)
        self.sidebar_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.sidebar_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # Create a widget to hold the content of the sidebar
        sidebar_content_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_content_widget)
        sidebar_layout.addWidget(QPushButton("Button 1"))
        sidebar_layout.addWidget(QPushButton("Button 2"))
        sidebar_layout.addStretch() # Adds flexible space to push content to the top

        # Set the content widget to the QDockWidget
        self.sidebar_dock.setWidget(sidebar_content_widget)

        # Add the QDockWidget to the left dock area of the QMainWindow
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar_dock)

        # 1. SETUP PERSISTENT PROFILE (Keeps you logged in)
        # Creates a folder 'airlock_cache' next to this script
        base_path = os.path.dirname(os.path.abspath(__file__))
        storage_path = os.path.join(base_path, "airlock_cache")
        
        self.profile = QWebEngineProfile("AirlockProfile", self)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        
        # Spoof Chrome to avoid being blocked
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # 2. SETUP BROWSER
        self.browser = QWebEngineView()
        self.page = QWebEnginePage(self.profile, self.browser)
        self.browser.setPage(self.page)
        self.setCentralWidget(self.browser)

        # 3. SETUP BRIDGE
        self.channel = QWebChannel()
        self.bridge = SecurityBridge()
        self.channel.registerObject("airlock", self.bridge)
        self.page.setWebChannel(self.channel)

        # 4. INJECT SCRIPTS
        self.browser.loadFinished.connect(self.inject_security_layer)

        # TODO: Add in option to select chatgpt or Gemini 

        # 5. LOAD URL
        print("[PYTHON] Loading ChatGPT...")  
        self.browser.setUrl(QUrl("https://chatgpt.com"))

    def inject_security_layer(self):
        print("[PYTHON] Page Loaded. Injecting Security Scripts...")

        # A. Inject QWebChannel (The communication library)
        # Note: We use the internal Qt resource if available
        qt_js = QFile(":/qtwebchannel/qwebchannel.js")
        if qt_js.open(QIODevice.OpenModeFlag.ReadOnly):
            self.page.runJavaScript(str(qt_js.readAll(), 'utf-8'))
        else:
            print("[PYTHON] ⚠️ Warning: Internal QWebChannel resource not found.")

        # B. Inject YOUR Guard Script
        guard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard.js")
        if os.path.exists(guard_path):
            with open(guard_path, "r", encoding='utf-8') as f:
                js_code = f.read()
                self.page.runJavaScript(js_code)
                print("[PYTHON] 💉 guard.js injected successfully.")
        else:
            print(f"[PYTHON] ❌ Error: guard.js not found at {guard_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AirlockApp()
    window.show()
    sys.exit(app.exec())