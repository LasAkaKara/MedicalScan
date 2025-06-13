from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from themes import PRIMARY_COLOR, SECONDARY_COLOR ,FONT_FAMILY, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG

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
        header.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {PRIMARY_COLOR}; font-family: {FONT_FAMILY};")
        main_layout.addWidget(header)

        subtitle = QLabel("Nhập mã xác thực và mật khẩu mới")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #406D96; font-family: {FONT_FAMILY}; font-weight: 600;")
        main_layout.addWidget(subtitle)

        # Verification code input
        self.verification_code = QLineEdit()
        self.verification_code.setPlaceholderText("Mã xác thực")
        self.verification_code.setStyleSheet(f"""
            QLineEdit {{
                border: 1.5px solid #ccc;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: {FONT_SIZE_SM}px;
                font-family: {FONT_FAMILY};
                background: #fff;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {PRIMARY_COLOR};
                background: #f7fbff;
            }}
        """)
        self.verification_code.setMaxLength(6)
        self.verification_code.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.verification_code)

        # New password input
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Mật khẩu mới")
        self.new_password.setStyleSheet(f"""
            QLineEdit {{
                border: 1.5px solid #ccc;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: {FONT_SIZE_SM}px;
                font-family: {FONT_FAMILY};
                background: #fff;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {PRIMARY_COLOR};
                background: #f7fbff;
            }}
        """)
        self.new_password.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.new_password)

        # Confirm password input
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Xác nhận mật khẩu mới")
        self.confirm_password.setStyleSheet(f"""
            QLineEdit {{
                border: 1.5px solid #ccc;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: {FONT_SIZE_SM}px;
                font-family: {FONT_FAMILY};
                background: #fff;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {PRIMARY_COLOR};
                background: #f7fbff;
            }}
        """)
        self.confirm_password.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.confirm_password)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e53935;")
        main_layout.addWidget(self.error_label)

        # Buttons
        self.reset_button = QPushButton("ĐẶT LẠI MẬT KHẨU")
        self.reset_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px;
                font-size: 20px;
                font-family: {FONT_FAMILY};
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:pressed {{
                background-color: #27405c;
            }}
        """)
        main_layout.addWidget(self.reset_button)

        self.resend_button = QPushButton("Gửi lại mã xác thực")
        self.resend_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;;
                color: {SECONDARY_COLOR};
                border: 1px solid {SECONDARY_COLOR};
                border-radius: 10px;
                padding: 10px;
                font-family: {FONT_FAMILY};
                font=size: {FONT_SIZE_MD}px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:pressed {{
                background-color: #27405c;
            }}
        """)
        self.resend_button.setContentsMargins(16, 0, 16, 0)
        main_layout.addWidget(self.resend_button)

        self.back_btn = QPushButton("Quay lại đăng nhập")
        self.back_btn.setFlat(True)
        self.back_btn.setStyleSheet(f"text-decoration: underline; background: transparent; font-size: {FONT_SIZE_MD}px; font-family: {FONT_FAMILY}; color: {PRIMARY_COLOR};")
        main_layout.addWidget(self.back_btn)