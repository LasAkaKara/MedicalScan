from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer

class LoadingOverlay(QWidget):
    def __init__(self, parent=None, message="Đang xử lý..."):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("background: rgba(0,0,0,120);")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.label = QLabel(message)
        self.label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Indeterminate
        self.progress.setFixedWidth(180)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        self.hide()

    def show_overlay(self, message="Đang xử lý..."):
        self.label.setText(message)
        self.resize(self.parent().size())
        self.show()
        self.raise_()

    def hide_overlay(self):
        self.hide()

    def resizeEvent(self, event):
        self.resize(self.parent().size())
        super().resizeEvent(event)