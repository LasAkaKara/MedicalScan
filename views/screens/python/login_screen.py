from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal, QObject
import os
import webbrowser
from dotenv import load_dotenv
from urllib.parse import urlencode
from controllers.auth_controller import AuthController
from views.screens.pyside.login_screen_ui import LoginScreenUI

load_dotenv()

class LoginScreen(LoginScreenUI):
    # Signals for navigation
    go_to_signup = Signal()
    go_to_reset_password = Signal(str)
    go_to_verify = Signal(str)
    login_success = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.is_submitting = False

        # Connect UI signals to logic
        self.login_btn.clicked.connect(self.validate_login)
        self.forgot_pw_btn.clicked.connect(self.handle_forgot_password)
        self.signup_btn.clicked.connect(lambda: self.go_to_signup.emit())
        self.google_btn.clicked.connect(self.initiate_google_oauth)

    def show_error(self, message):
        self.error_label.setText(message)

    def clear_fields(self):
        self.email_input.clear()
        self.password_input.clear()
        self.error_label.clear()
        self.is_submitting = False

    def handle_forgot_password(self):
        email = self.email_input.text().strip()
        if not email:
            self.show_error("Vui lòng nhập email để đặt lại mật khẩu")
            return

        # Validate email format
        if not self.auth_controller.validate_email(email):
            self.show_error("Email không hợp lệ")
            return

        # Check if email exists and send reset code
        success, message = self.auth_controller.send_reset_password_code(email)
        if success:
            self.show_error("")  # Clear any previous error
            self.go_to_reset_password.emit(email)
        else:
            self.show_error(message)

    def validate_login(self):
        if self.is_submitting:
            return
        self.is_submitting = True
        self.login_btn.setEnabled(False)
        email = self.email_input.text()
        password = self.password_input.text()
        if not email or not password:
            self.show_error("Vui lòng điền đầy đủ thông tin")
            self.is_submitting = False
            self.login_btn.setEnabled(True)
            return

        # Check email verification status
        email_status = self.check_email_verification_status(email)
        if email_status == "unverified":
            self.go_to_verify.emit(email)
            self.is_submitting = False
            self.login_btn.setEnabled(True)
            return

        # Normal login flow
        success, message = self.auth_controller.login(email, password)
        if success:
            self.login_success.emit(email)
            self.clear_fields()
        else:
            self.show_error(message)
        self.is_submitting = False
        self.login_btn.setEnabled(True)

    def check_email_verification_status(self, email):
        try:
            if hasattr(self.auth_controller.db_service, 'check_verification_status'):
                return self.auth_controller.db_service.check_verification_status(email)
            return "unknown"
        except Exception as e:
            return "unknown"

    def initiate_google_oauth(self):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        if not client_id or not redirect_uri:
            self.show_error("Google OAuth chưa được cấu hình.")
            return
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        webbrowser.open(auth_url)
        QMessageBox.information(self, "Google OAuth", "Vui lòng cấp quyền trong trình duyệt và sao chép mã ủy quyền.")