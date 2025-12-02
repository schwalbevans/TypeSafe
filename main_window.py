import sys
import json
import requests
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
    QLineEdit,
)
from PyQt6.QtCore import Qt, QTimer



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Airlock AI")
        self.setGeometry(100, 100, 900, 700)
        
        self.proxy_thread = None
        self.api_key = None
        self.upstream_host = "https://api.openai.com" # Default
        self.regex_pattern = ""
        self.conversation_history = []

        # --- Main Layout ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(splitter)

        # --- Left Panel (AI Services List) ---
        self.ai_service_list = QListWidget()
        self.ai_service_list.addItem("ChatGPT") 
        self.ai_service_list.setMaximumWidth(200)
        splitter.addWidget(self.ai_service_list)
        self.ai_service_list.itemClicked.connect(self.on_service_selected)

        # --- Right Panel (Main Content Area) ---
        main_content_area = QWidget()
        layout = QVBoxLayout()
        main_content_area.setLayout(layout)
        splitter.addWidget(main_content_area)

        # Regex pattern input
        layout.addWidget(QLabel("Regex Pattern:"))
        regex_layout = QHBoxLayout()
        self.regex_input = QLineEdit()
        regex_layout.addWidget(self.regex_input)
        self.set_pattern_button = QPushButton("Set Pattern")
        self.set_pattern_button.clicked.connect(self.set_regex_pattern)
        regex_layout.addWidget(self.set_pattern_button)
        layout.addLayout(regex_layout)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Message input
        message_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.returnPressed.connect(self.send_message)
        message_layout.addWidget(self.message_input)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        message_layout.addWidget(self.send_button)
        layout.addLayout(message_layout)
    
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)
        
        splitter.setSizes([150, 750])

    def set_regex_pattern(self):
        self.regex_pattern = self.regex_input.text()
        self.log_to_display(f"Regex pattern set: {self.regex_pattern}")

    def send_message(self):
        user_message = self.message_input.text()
        if not user_message:
            return

        self.chat_display.append(f"You: {user_message}")
        self.message_input.clear()
        self.conversation_history.append({"role": "user", "content": user_message})
        
        self.send_button.setEnabled(False)
        self.message_input.setEnabled(False)

        # Make the API call through the proxy
        self.log_to_display("Sending message to the API...")
        try:
            proxies = {
                "http": f"http://localhost:{self.proxy_thread.port}",
                "https": f"http://localhost:{self.proxy_thread.port}",
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": self.conversation_history,
            }
            url = f"{self.upstream_host}/v1/chat/completions"

            self.log_to_display(f"Request URL: {url}")
            self.log_to_display(f"Request Headers: {{'Content-Type': 'application/json', 'Authorization': 'Bearer {self.api_key[:4]}...{self.api_key[-4:]}'}}")
            self.log_to_display(f"Request Data: {json.dumps(data)}")

            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(data),
                proxies=proxies,
                verify=False, # In a real app, you'd handle SSL verification properly
            )
            response.raise_for_status()
            api_response = response.json()
            ai_message = api_response["choices"][0]["message"]["content"]
            self.chat_display.append(f"AI: {ai_message}")
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            self.log_to_display("Message received from the API.")

        except requests.exceptions.RequestException as e:
            self.log_to_display(f"[ERROR] API request failed: {e}")
            self.chat_display.append(f"<font color='red'>Error: {e}</font>")
        finally:
            self.message_input.setEnabled(True)
            QTimer.singleShot(2000, lambda: self.send_button.setEnabled(True))


    def start_proxy(self):
        if self.proxy_thread is None:
            port = 8080  # You can make this configurable later
            self.proxy_thread = ProxyThread(port=port, upstream_host=self.upstream_host, regex_pattern=self.regex_pattern)
            self.proxy_thread.log_message.connect(self.log_to_display)
            self.proxy_thread.start()
            self.log_to_display(f"Proxy started on port {port}. Configure your system or application to use http://localhost:{port} as the proxy server.")
            self.ai_service_list.setEnabled(False)

    def stop_proxy(self):
        if self.proxy_thread:
            self.proxy_thread.stop()
            self.proxy_thread = None
            self.log_to_display("Proxy stopped.")
            self.ai_service_list.setEnabled(True)

    def log_to_display(self, message):
        self.log_display.append(message)

    def on_service_selected(self, item: QListWidgetItem):
        self.stop_proxy()
        service_name = item.text()
        if service_name == "ChatGPT":
            self.upstream_host = "https://api.openai.com"
            self.handle_chatgpt_login()
       
    def handle_chatgpt_login(self):
        api_key, ok = QInputDialog.getText(self, "ChatGPT API Key", "Enter your OpenAI API Key:")
        if ok and api_key:
            self.api_key = api_key
            self.log_to_display(f"ChatGPT API Key set: {self.api_key[:4]}...{self.api_key[-4:]}")
            self.start_proxy()
        else:
            self.log_to_display("ChatGPT API Key not provided.")
            self.ai_service_list.setEnabled(True)
            
    def closeEvent(self, event):
        """Ensure proxy is stopped when window is closed."""
        self.stop_proxy()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
