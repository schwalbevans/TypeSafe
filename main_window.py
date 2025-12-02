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

        
        splitter.setSizes([150, 750])

 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
