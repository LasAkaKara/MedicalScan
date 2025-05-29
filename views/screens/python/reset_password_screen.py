from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QMessageBox
from controllers.auth_controller import AuthController
from views.screens.pyside.reset_password_screen_ui import ResetPasswordScreenUI

class ResetPasswordScreen(ResetPasswordScreenUI):
    go_to_login = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.current_email = ""
        self.is_submitting = False
        self.is_resending = False
        self.cooldown_seconds = 0
        self.cooldown_timer = QTimer(self)
        self.cooldown_timer.timeout.connect(self.update_cooldown)

        # Connect UI signals
        self.reset_button.clicked.connect(self.reset_password)
        self.resend_button.clicked.connect(self.send_reset_code)
        self.back_btn.clicked.connect(lambda: self.go_to_login.emit())

    def set_email(self, email):
        self.current_email = email
        self.verification_code.clear()
        self.new_password.clear()
        self.confirm_password.clear()
        self.error_label.clear()
        self.is_submitting = False
        self.is_resending = False
        self.cooldown_seconds = 0
        self.resend_button.setEnabled(True)
        self.reset_button.setEnabled(True)

    def send_reset_code(self):
        if self.cooldown_seconds > 0 or self.is_resending:
            return
        if not self.current_email:
            self.show_error("Không có email để gửi mã xác thực")
            return
        self.is_resending = True
        self.resend_button.setEnabled(False)
        success, message = self.auth_controller.send_reset_password_code(self.current_email)
        if success:
            self.show_success("Đã gửi mã xác thực đến email của bạn")
            self.start_cooldown(60)
        else:
            self.show_error(message)
            self.resend_button.setEnabled(True)
        self.is_resending = False

    def reset_password(self):
        if self.is_submitting:
            return
        self.is_submitting = True
        self.reset_button.setEnabled(False)

        code = self.verification_code.text().strip()
        new_password = self.new_password.text()
        confirm_password = self.confirm_password.text()

        if not code:
            self.show_error("Vui lòng nhập mã xác thực")
            self.reset_submission_state()
            return
        if not new_password:
            self.show_error("Vui lòng nhập mật khẩu mới")
            self.reset_submission_state()
            return
        if len(new_password) < 6:
            self.show_error("Mật khẩu phải có ít nhất 6 ký tự")
            self.reset_submission_state()
            return
        if new_password != confirm_password:
            self.show_error("Mật khẩu không khớp")
            self.reset_submission_state()
            return

        success, message = self.auth_controller.reset_password(
            self.current_email, code, new_password
        )
        if success:
            self.show_success("Đặt lại mật khẩu thành công")
            QTimer.singleShot(2000, self.go_to_login.emit)
        else:
            self.show_error(message)
            self.reset_submission_state()

    def reset_submission_state(self):
        self.is_submitting = False
        self.reset_button.setEnabled(True)

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

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: #e53935;")

    def show_success(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: #4CAF50;")