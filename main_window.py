import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QWidget,
    QSplitter,
    QInputDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from proxy import ProxyThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Airlock AI")
        self.setGeometry(100, 100, 900, 700)
        
        self.proxy_thread = None
        self.api_key = None
        self.upstream_host = "https://api.openai.com" # Default

        # --- Main Layout ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(splitter)

        # --- Left Panel (AI Services List) ---
        self.ai_service_list = QListWidget()
        self.ai_service_list.addItem("ChatGPT")
        self.ai_service_list.addItem("Gemini")
        self.ai_service_list.setMaximumWidth(200)
        splitter.addWidget(self.ai_service_list)
        self.ai_service_list.itemClicked.connect(self.on_service_selected)

        # --- Right Panel (Main Content Area) ---
        main_content_area = QWidget()
        layout = QVBoxLayout()
        main_content_area.setLayout(layout)
        splitter.addWidget(main_content_area)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Proxy")
        self.start_button.clicked.connect(self.start_proxy)
        self.stop_button = QPushButton("Stop Proxy")
        self.stop_button.clicked.connect(self.stop_proxy)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)
        
        splitter.setSizes([150, 750])

        # Automatically start the proxy on launch
        self.start_proxy()

    def start_proxy(self):
        if self.proxy_thread is None:
            port = 8080  # You can make this configurable later
            self.proxy_thread = ProxyThread(port=port, upstream_host=self.upstream_host)
            self.proxy_thread.log_message.connect(self.log_to_display)
            self.proxy_thread.start()
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.ai_service_list.setEnabled(False)

    def stop_proxy(self):
        if self.proxy_thread:
            self.proxy_thread.stop()
            self.proxy_thread = None
            self.log_to_display("Proxy stopped.")
            
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.ai_service_list.setEnabled(True)

    def log_to_display(self, message):
        self.log_display.append(message)

    def on_service_selected(self, item: QListWidgetItem):
        service_name = item.text()
        if service_name == "ChatGPT":
            self.upstream_host = "https://api.openai.com"
            self.handle_chatgpt_login()
        elif service_name == "Gemini":
            # Example for Gemini, you'd change the host
            self.upstream_host = "https://generativelanguage.googleapis.com"
            self.log_to_display("Set upstream to Gemini. Login not implemented.")

    def handle_chatgpt_login(self):
        api_key, ok = QInputDialog.getText(self, "ChatGPT API Key", "Enter your OpenAI API Key:")
        if ok and api_key:
            self.api_key = api_key
            self.log_to_display(f"ChatGPT API Key set: {self.api_key[:4]}...{self.api_key[-4:]}")
        else:
            self.log_to_display("ChatGPT API Key not provided.")
            
    def closeEvent(self, event):
        """Ensure proxy is stopped when window is closed."""
        self.stop_proxy()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
