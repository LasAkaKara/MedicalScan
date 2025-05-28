from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class ResetPasswordScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đặt Lại Mật Khẩu")
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("Đặt Lại Mật Khẩu")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        main_layout.addWidget(header)

        subtitle = QLabel("Nhập mã xác thực và mật khẩu mới")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #406D96;")
        main_layout.addWidget(subtitle)

        # Verification code input
        self.verification_code = QLineEdit()
        self.verification_code.setPlaceholderText("Mã xác thực")
        self.verification_code.setMaxLength(6)
        self.verification_code.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.verification_code)

        # New password input
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Mật khẩu mới")
        self.new_password.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.new_password)

        # Confirm password input
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Xác nhận mật khẩu mới")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.confirm_password)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e53935;")
        main_layout.addWidget(self.error_label)

        # Buttons
        self.reset_button = QPushButton("ĐẶT LẠI MẬT KHẨU")
        main_layout.addWidget(self.reset_button)

        self.resend_button = QPushButton("Gửi lại mã xác thực")
        main_layout.addWidget(self.resend_button)

        self.back_btn = QPushButton("Quay lại đăng nhập")
        self.back_btn.setFlat(True)
        self.back_btn.setStyleSheet("color: #1976d2; text-decoration: underline; background: transparent;")
        main_layout.addWidget(self.back_btn)