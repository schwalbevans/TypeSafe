import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Airlock AI")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # Create a central widget with a label
        central_widget = QLabel("Welcome to Airlock AI")
        central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
