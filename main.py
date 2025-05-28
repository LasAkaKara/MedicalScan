import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from views.screens.python.login_screen import LoginScreen
from views.screens.python.signup_screen import SignupScreen
from views.screens.python.home_screen import HomeScreen
from views.screens.python.verification_screen import VerificationScreen
from views.screens.python.reset_password_screen import ResetPasswordScreen

class MedicalApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.stack = QStackedWidget()

        # Instantiate screens
        self.login_screen = LoginScreen()
        self.signup_screen = SignupScreen()
        self.home_screen = HomeScreen()
        self.verification_screen = VerificationScreen()
        self.reset_password_screen = ResetPasswordScreen()

        # Add screens to stack
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.signup_screen)
        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.verification_screen)
        self.stack.addWidget(self.reset_password_screen)

        # Connect navigation signals
        self.login_screen.go_to_signup.connect(self.show_signup)
        self.signup_screen.go_to_login.connect(self.show_login)
        self.login_screen.login_success.connect(self.show_home)
        self.home_screen.go_to_login.connect(self.show_login)
        self.home_screen.go_to_scan.connect(self.show_scan)  # Placeholder for scan screen

        # Verification navigation
        self.login_screen.go_to_verify.connect(self.show_verification)
        self.signup_screen.go_to_verify.connect(self.show_verification)
        self.verification_screen.go_to_login.connect(self.show_login)

        # Reset password navigation
        self.login_screen.go_to_reset_password.connect(self.show_reset_password)
        self.reset_password_screen.go_to_login.connect(self.show_login)

        self.stack.setCurrentWidget(self.login_screen)
        self.stack.setFixedSize(400, 700)
        self.stack.show()

    def show_signup(self):
        self.stack.setCurrentWidget(self.signup_screen)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_screen)

    def show_home(self, email=None):
        self.stack.setCurrentWidget(self.home_screen)

    def show_verification(self, email):
        self.verification_screen.set_email(email)
        self.stack.setCurrentWidget(self.verification_screen)

    def show_reset_password(self, email):
        self.reset_password_screen.set_email(email)
        self.stack.setCurrentWidget(self.reset_password_screen)

    def show_scan(self):
        # Placeholder: implement scan screen and navigation
        pass

if __name__ == '__main__':
    app = MedicalApp(sys.argv)

    app.setStyleSheet("QStackedWidget { background-color: #fbfcff; }")
    sys.exit(app.exec())