from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QStackedWidget, QSizePolicy, QToolButton
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
from themes import PRIMARY_COLOR, SECONDARY_COLOR ,FONT_SIZE_XL ,FONT_SIZE_LG, FONT_SIZE_MD, FONT_SIZE_SM, FONT_FAMILY

class LoginScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MediScan - Đăng nhập")
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

        # Section: Đăng nhập với
        section_label = QLabel("Đăng nhập với")
        section_label.setAlignment(Qt.AlignCenter)
        section_label.setStyleSheet("font-size: 18px; font-weight: 500; margin-top: 12px;")
        main_layout.addWidget(section_label)

        # Login method selection
        method_layout = QHBoxLayout()
        method_layout.setSpacing(20)
        method_layout.setAlignment(Qt.AlignCenter)

        # Google button
        self.google_btn = QPushButton(" Google")
        self.google_btn.setIcon(QIcon("assets/googleicon.png"))  # <-- Change to your Google icon path
        self.google_btn.setStyleSheet("""
            QPushButton {
                background: #fff;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #f5f5f5;
            }
        """)
        method_layout.addWidget(self.google_btn)

        # Email button
        self.email_btn = QPushButton(" Email")
        self.email_btn.setIcon(QIcon("assets/Email.png"))  # <-- Change to your mail icon path
        self.email_btn.setStyleSheet("""
            QPushButton {
                background: #fff;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #f5f5f5;
            }
        """)
        method_layout.addWidget(self.email_btn)

        main_layout.addLayout(method_layout)

        # Stacked widget for login form (hidden by default)
        self.form_stack = QStackedWidget()
        self.form_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Empty widget (default)
        self.empty_widget = QWidget()
        self.form_stack.addWidget(self.empty_widget)

        # Email login form widget
        self.email_form_widget = QWidget()
        email_form_layout = QVBoxLayout(self.email_form_widget)
        email_form_layout.setSpacing(8)

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
        email_form_layout.addWidget(self.email_input)

        password_layout = QHBoxLayout()
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(0)

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
        password_layout.addWidget(self.password_input)

        self.toggle_pw_btn = QToolButton()
        self.toggle_pw_btn.setIcon(QIcon("assets/eye-close.png"))  
        self.toggle_pw_btn.setCheckable(True)
        self.toggle_pw_btn.setIconSize(QSize(28, 28))
        self.toggle_pw_btn.setFixedSize(34, 34)
        self.toggle_pw_btn.setStyleSheet("""
            QToolButton {
                border: none;
                padding-right: 8px;
                margin-left: 8px;  /* Add spacing between input and icon */
                background: transparent;
            }
        """)
        self.toggle_pw_btn.setCursor(Qt.PointingHandCursor)
        password_layout.addWidget(self.toggle_pw_btn)

        email_form_layout.addLayout(password_layout)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e53935;")
        email_form_layout.addWidget(self.error_label)

        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        self.forgot_pw_btn = QPushButton("Quên mật khẩu?")
        self.forgot_pw_btn.setFlat(True)
        self.forgot_pw_btn.setStyleSheet("text-decoration: underline; background: transparent; font-size: {FONT_SIZE_MD}px")
        forgot_layout.addWidget(self.forgot_pw_btn)
        email_form_layout.addLayout(forgot_layout)

        self.login_btn = QPushButton("ĐĂNG NHẬP")
        self.login_btn.setStyleSheet(f"""
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
        email_form_layout.addWidget(self.login_btn)

        self.form_stack.addWidget(self.email_form_widget)
        main_layout.addWidget(self.form_stack)

        # Spacer
        main_layout.addStretch()

        # Signup link at the bottom
        self.signup_btn = QPushButton("Chưa có tài khoản? Đăng ký tại đây")
        self.signup_btn.setFlat(True)
        self.signup_btn.setStyleSheet(f"text-decoration: underline; background: transparent; font-size: {FONT_SIZE_MD}px")
        main_layout.addWidget(self.signup_btn, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        # --- Logic for switching forms ---
        self.email_btn.clicked.connect(self.show_email_form)
        self.google_btn.clicked.connect(self.hide_email_form)

        # By default, show nothing (or you can show Google by default)
        self.form_stack.setCurrentWidget(self.empty_widget)
        self.toggle_pw_btn.toggled.connect(self.toggle_password_visibility)

    def show_email_form(self):
        self.form_stack.setCurrentWidget(self.email_form_widget)

    def hide_email_form(self):
        self.form_stack.setCurrentWidget(self.empty_widget)
    
    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_pw_btn.setIcon(QIcon("assets/eye-open.png"))  # Use your eye-open icon
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_pw_btn.setIcon(QIcon("assets/eye-close.png"))  # Use your eye-closed icon