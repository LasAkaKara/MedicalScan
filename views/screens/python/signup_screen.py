from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal, QThread, QObject
from controllers.auth_controller import AuthController
from views.screens.pyside.signup_screen import SignupScreenUI
import re

class EmailCheckWorker(QObject):
    finished = Signal(bool)
    error = Signal(str)

    def __init__(self, auth_controller, email):
        super().__init__()
        self.auth_controller = auth_controller
        self.email = email

    def run(self):
        try:
            exists = self.auth_controller.check_email_exists(self.email)
            self.finished.emit(exists)
        except Exception as e:
            self.error.emit(str(e))

class RegistrationWorker(QObject):
    finished = Signal(bool, str)
    error = Signal(str)

    def __init__(self, auth_controller, email, password, confirm_password):
        super().__init__()
        self.auth_controller = auth_controller
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

    def run(self):
        try:
            success, message = self.auth_controller.register(
                self.email, self.password, self.confirm_password
            )
            self.finished.emit(success, message)
        except Exception as e:
            self.error.emit(str(e))

class SignupScreen(SignupScreenUI):
    go_to_login = Signal()
    go_to_verify = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.is_submitting = False
        self.is_checking_email = False

        # Connect UI signals to logic
        self.signup_button.clicked.connect(self.register)
        self.login_btn.clicked.connect(lambda: self.go_to_login.emit())

    def show_error(self, message):
        self.error_label.setText(message)

    def clear_fields(self):
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.error_label.clear()
        self.is_submitting = False
        self.is_checking_email = False

    def register(self):
        if self.is_submitting or self.is_checking_email:
            return

        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Validate input fields
        if not email or not password or not confirm_password:
            self.show_error("Vui lòng điền đầy đủ thông tin")
            return

        # Validate email format
        if not self.is_valid_email(email):
            self.show_error("Email không hợp lệ")
            return

        # Validate password length
        if len(password) < 6:
            self.show_error("Mật khẩu phải có ít nhất 6 ký tự")
            return

        # Validate password match
        if password != confirm_password:
            self.show_error("Mật khẩu không khớp")
            return

        self.is_checking_email = True
        self.signup_button.setEnabled(False)
        self.error_label.clear()

        # Start email check in a thread
        self.email_check_thread = QThread()
        self.email_check_worker = EmailCheckWorker(self.auth_controller, email)
        self.email_check_worker.moveToThread(self.email_check_thread)
        self.email_check_thread.started.connect(self.email_check_worker.run)
        self.email_check_worker.finished.connect(self.on_email_check_finished)
        self.email_check_worker.error.connect(self.on_worker_error)
        self.email_check_worker.finished.connect(self.email_check_thread.quit)
        self.email_check_worker.finished.connect(self.email_check_worker.deleteLater)
        self.email_check_thread.finished.connect(self.email_check_thread.deleteLater)
        self.email_check_thread.start()

    def on_email_check_finished(self, exists):
        self.is_checking_email = False
        if exists:
            self.show_error("Email đã tồn tại. Vui lòng sử dụng email khác.")
            self.signup_button.setEnabled(True)
        else:
            # Proceed to registration
            self.is_submitting = True
            self.signup_button.setEnabled(False)
            email = self.email_input.text().strip()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()

            self.registration_thread = QThread()
            self.registration_worker = RegistrationWorker(
                self.auth_controller, email, password, confirm_password
            )
            self.registration_worker.moveToThread(self.registration_thread)
            self.registration_thread.started.connect(self.registration_worker.run)
            self.registration_worker.finished.connect(self.on_registration_finished)
            self.registration_worker.error.connect(self.on_worker_error)
            self.registration_worker.finished.connect(self.registration_thread.quit)
            self.registration_worker.finished.connect(self.registration_worker.deleteLater)
            self.registration_thread.finished.connect(self.registration_thread.deleteLater)
            self.registration_thread.start()

    def on_registration_finished(self, success, message):
        self.is_submitting = False
        self.signup_button.setEnabled(True)
        if success:
            # Go to verify screen
            self.go_to_verify.emit(self.email_input.text().strip())
            self.clear_fields()
        else:
            self.show_error(message)

    def on_worker_error(self, error_message):
        self.is_submitting = False
        self.is_checking_email = False
        self.signup_button.setEnabled(True)
        self.show_error("Đã xảy ra lỗi. Vui lòng thử lại sau.")

    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None