from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QMessageBox
from controllers.auth_controller import AuthController
from views.screens.pyside.verification_screen_ui import VerificationScreenUI

class VerificationScreen(VerificationScreenUI):
    go_to_login = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.current_email = ""
        self.is_verifying = False
        self.is_resending = False
        self.cooldown_seconds = 0
        self.cooldown_timer = QTimer(self)
        self.cooldown_timer.timeout.connect(self.update_cooldown)

        # Connect UI signals
        self.verify_button.clicked.connect(self.verify_code)
        self.resend_button.clicked.connect(self.resend_code)
        self.back_btn.clicked.connect(lambda: self.go_to_login.emit())

    def set_email(self, email):
        self.current_email = email

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: #e53935;")

    def show_success(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: #4CAF50;")

    def verify_code(self):
        if self.is_verifying:
            return
        code = self.verification_code.text().strip()
        if not code:
            self.show_error("Vui lòng nhập mã xác thực")
            return
        self.is_verifying = True
        self.verify_button.setEnabled(False)
        success, message = self.auth_controller.verify_code(self.current_email, code)
        if success:
            self.show_success("Xác thực thành công!")
            QTimer.singleShot(1500, self.go_to_login.emit)
        else:
            self.show_error(message)
        self.is_verifying = False
        self.verify_button.setEnabled(True)

    def resend_code(self):
        if self.cooldown_seconds > 0 or self.is_resending:
            return
        if not self.current_email:
            self.show_error("Không có email để gửi mã xác thực")
            return
        self.is_resending = True
        self.resend_button.setEnabled(False)
        success, message = self.auth_controller.resend_verification(self.current_email)
        if success:
            self.show_success("Đã gửi lại mã xác thực mới")
            self.start_cooldown(60)
        else:
            self.show_error(message)
            self.resend_button.setEnabled(True)
        self.is_resending = False

    def start_cooldown(self, seconds):
        self.cooldown_seconds = seconds
        self.resend_button.setText(f"Gửi lại mã xác thực ({self.cooldown_seconds}s)")
        self.resend_button.setEnabled(False)
        self.cooldown_timer.start(1000)

    def update_cooldown(self):
        self.cooldown_seconds -= 1
        if self.cooldown_seconds > 0:
            self.resend_button.setText(f"Gửi lại mã xác thực ({self.cooldown_seconds}s)")
        else:
            self.resend_button.setText("Gửi lại mã xác thực")
            self.resend_button.setEnabled(True)
            self.cooldown_timer.stop()