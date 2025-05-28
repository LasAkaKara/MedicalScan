from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from views.components.header import Header

class HomeScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MediScan - Home")
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        # Header
        self.header = Header("MediScan")
        main_layout.addWidget(self.header)

        subtitle = QLabel("Your health companion")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #406D96;")
        main_layout.addWidget(subtitle)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Start Scanning Button
        self.scan_btn = QPushButton("Start Scanning")
        self.scan_btn.setStyleSheet("font-size: 18px; padding: 12px; background: #406D96; color: white; border-radius: 8px;")
        self.scan_btn.setFixedWidth(200)
        self.scan_btn.setCursor(Qt.PointingHandCursor)
        self.scan_btn.setContentsMargins(0, 20, 0, 20)
        self.scan_btn.setMinimumHeight(48)
        self.scan_btn.setMaximumWidth(300)
        self.scan_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scan_btn_layout = QHBoxLayout()
        scan_btn_layout.addStretch()
        scan_btn_layout.addWidget(self.scan_btn)
        scan_btn_layout.addStretch()
        main_layout.addLayout(scan_btn_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Logout Button
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setStyleSheet("color: #F44336; background: transparent; font-size: 14px;")
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(self.logout_btn, alignment=Qt.AlignCenter)