from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal

class Header(QWidget):
    menu_clicked = Signal()
    profile_clicked = Signal()

    def __init__(self, title="MediScan", parent=None):
        super().__init__(parent)
        self.setFixedHeight(56)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(0)

        # Menu button
        self.menu_btn = QPushButton()
        self.menu_btn.setText("☰")  # Unicode menu icon
        self.menu_btn.setFixedWidth(40)
        self.menu_btn.setFlat(True)
        self.menu_btn.clicked.connect(self.menu_clicked.emit)
        layout.addWidget(self.menu_btn, alignment=Qt.AlignLeft)

        # Title label
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title_label, stretch=1)

        # Profile button
        self.profile_btn = QPushButton()
        self.profile_btn.setText("👤")  # Unicode profile icon
        self.profile_btn.setFixedWidth(40)
        self.profile_btn.setFlat(True)
        self.profile_btn.clicked.connect(self.profile_clicked.emit)
        layout.addWidget(self.profile_btn, alignment=Qt.AlignRight)