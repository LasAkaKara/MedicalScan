from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QStackedWidget, QSizePolicy, QToolButton
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from themes import PRIMARY_COLOR, SECONDARY_COLOR ,FONT_SIZE_XL ,FONT_SIZE_LG, FONT_SIZE_MD, FONT_SIZE_SM, FONT_FAMILY

class SignupScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MediScan - Đăng ký")
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(16)
        

        # Top Image
        self.top_image = QLabel()
        self.top_image.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/login-bg.png")
        if not pixmap.isNull():
            self.top_image.setPixmap(pixmap.scaled(240, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.top_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(self.top_image)

        # Header
        self.header_label = QLabel("MediScan")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet(f"font-size: {FONT_SIZE_XL}px; font-weight: bold; color:{PRIMARY_COLOR}")
        main_layout.addWidget(self.header_label)

        # Subtitle
        self.subtitle_label = QLabel("Hiểu Rõ Mọi Thành Phần\nNhắc Nhở Theo Dõi Sức Khỏe")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; color: {SECONDARY_COLOR}; font-family: {FONT_FAMILY};")
        main_layout.addWidget(self.subtitle_label)

        # Form label
        self.form_label = QLabel("Đăng ký tài khoản")
        self.form_label.setAlignment(Qt.AlignCenter)
        self.form_label.setStyleSheet("font-size: 18px;")
        main_layout.addWidget(self.form_label)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet(f"""
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
        main_layout.addWidget(self.email_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(f"""
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
        main_layout.addWidget(self.password_input)

        # Confirm password input
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Xác nhận mật khẩu")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(f"""
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
        main_layout.addWidget(self.confirm_password_input)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e53935;")
        main_layout.addWidget(self.error_label)

        # Signup button
        self.signup_button = QPushButton("ĐĂNG KÝ")
        self.signup_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px;
                font-size: {FONT_SIZE_LG}px;
                font-family: {FONT_FAMILY};
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:pressed {{
                background-color: #27405c;
            }}
        """)
        main_layout.addWidget(self.signup_button)

        # Already have account
        self.login_btn = QPushButton("Đã có tài khoản? Đăng nhập")
        self.login_btn.setFlat(True)
        self.login_btn.setStyleSheet(f"text-decoration: underline; background: transparent; font-size: {FONT_SIZE_MD}px")
        main_layout.addWidget(self.login_btn)