from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class VerificationScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xác Thực Email")
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("Xác Thực Email")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        main_layout.addWidget(header)

        subtitle = QLabel("Vui lòng nhập mã xác thực đã được gửi đến email của bạn")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #406D96;")
        main_layout.addWidget(subtitle)

        # Verification code input
        self.verification_code = QLineEdit()
        self.verification_code.setPlaceholderText("Nhập mã xác thực")
        self.verification_code.setMaxLength(6)
        self.verification_code.setAlignment(Qt.AlignCenter)
        self.verification_code.setFixedHeight(40)
        main_layout.addWidget(self.verification_code)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e53935;")
        main_layout.addWidget(self.error_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.verify_button = QPushButton("XÁC THỰC")
        btn_layout.addWidget(self.verify_button)
        self.resend_button = QPushButton("Gửi lại mã xác thực")
        btn_layout.addWidget(self.resend_button)
        main_layout.addLayout(btn_layout)

        # Back to login
        self.back_btn = QPushButton("Quay lại đăng nhập")
        self.back_btn.setFlat(True)
        self.back_btn.setStyleSheet("color: #1976d2; text-decoration: underline; background: transparent;")
        main_layout.addWidget(self.back_btn)