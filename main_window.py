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
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Airlock AI")
        self.setGeometry(100, 100, 900, 700)

        # --- Main Layout ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(splitter)

        # --- Left Panel (AI Services List) ---
        self.ai_service_list = QListWidget()
        self.ai_service_list.addItem("ChatGPT")
        self.ai_service_list.addItem("Gemini")
        self.ai_service_list.setMaximumWidth(200)
        splitter.addWidget(self.ai_service_list)

        # Connect the item click signal to a handler
        self.ai_service_list.itemClicked.connect(self.on_service_selected)

        # --- Right Panel (Main Content Area) ---
        main_content_area = QWidget()
        layout = QVBoxLayout()
        main_content_area.setLayout(layout)

        self.status_label = QLabel("Please select a service to log in.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        splitter.addWidget(main_content_area)
        
        # Adjust splitter initial sizes
        splitter.setSizes([150, 750])

    def on_service_selected(self, item: QListWidgetItem):
        """Handles clicks on the AI service list."""
        service_name = item.text()
        if service_name == "ChatGPT":
            self.handle_chatgpt_login()
        elif service_name == "Gemini":
            self.status_label.setText("Gemini login is not yet implemented.")

    def handle_chatgpt_login(self):
        """Opens a dialog to get the ChatGPT API key."""
        api_key, ok = QInputDialog.getText(
            self, 
            "ChatGPT API Key", 
            "Enter your OpenAI API Key:"
        )

        if ok and api_key:
            # In a real app, you would securely store and use this key.
            # For now, we'll just confirm it was entered.
            print(f"ChatGPT API Key set: {api_key[:4]}...{api_key[-4:]}")
            self.status_label.setText("ChatGPT API Key has been set.")
        else:
            self.status_label.setText("ChatGPT API Key not provided.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
