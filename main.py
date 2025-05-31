import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from views.screens.python.login_screen import LoginScreen
from views.screens.python.signup_screen import SignupScreen
from views.screens.python.home_screen import HomeScreen
from views.screens.python.verification_screen import VerificationScreen
from views.screens.python.reset_password_screen import ResetPasswordScreen
from views.screens.python.scan_screen import ScanScreen
from views.screens.python.prescription_screen import PrescriptionScreen
from views.screens.python.profile_screen import ProfileScreen
from views.screens.python.settings_screen import SettingsScreen
from views.screens.python.prescription_detail_screen import PrescriptionDetailScreen

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
        self.scan_screen = ScanScreen()
        self.prescription_screen = PrescriptionScreen()
        self.profile_screen = ProfileScreen()
        self.settings_screen = SettingsScreen()
        self.prescription_detail_screen = PrescriptionDetailScreen()
        self.stack.addWidget(self.prescription_detail_screen)

        # Add screens to stack
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.signup_screen)
        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.verification_screen)
        self.stack.addWidget(self.reset_password_screen)
        self.stack.addWidget(self.scan_screen)
        self.stack.addWidget(self.prescription_screen)
        self.stack.addWidget(self.profile_screen)
        self.stack.addWidget(self.settings_screen)

        # Connect navigation signals
        self.login_screen.go_to_signup.connect(self.show_signup)
        self.signup_screen.go_to_login.connect(self.show_login)
        self.login_screen.login_success.connect(self.show_home)
        self.home_screen.go_to_login.connect(self.show_login)
        self.home_screen.go_to_scan.connect(self.show_scan)
        self.scan_screen.go_to_home.connect(self.show_home)
        self.home_screen.go_to_prescription.connect(self.show_prescription)
        self.home_screen.go_to_profile.connect(self.show_profile)
        self.home_screen.go_to_settings.connect(self.show_settings)
        self.prescription_screen.go_to_home.connect(self.show_home)
        self.prescription_screen.go_to_add_prescription.connect(self.show_add_prescription)
        self.profile_screen.go_to_login.connect(self.show_login)
        self.profile_screen.go_to_home.connect(self.show_home)
        self.settings_screen.go_to_home.connect(self.show_home)
        self.prescription_detail_screen.go_to_history.connect(self.show_prescription)


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
        self.stack.setCurrentWidget(self.scan_screen)
    
    def show_prescription(self):
        self.stack.setCurrentWidget(self.prescription_screen)

    def show_add_prescription(self):
        # Implement this to show your add prescription screen
        pass

    def show_profile(self):
        self.profile_screen.load_user_data()  # Refresh data each time
        self.stack.setCurrentWidget(self.profile_screen)
    
    def show_settings(self):
        self.settings_screen.load_settings()
        self.stack.setCurrentWidget(self.settings_screen)
    
    def show_prescription_detail(self, prescription_id):
        self.prescription_detail_screen.set_prescription_id(prescription_id)
        self.stack.setCurrentWidget(self.prescription_detail_screen)



if __name__ == '__main__':
    app = MedicalApp(sys.argv)

    app.setStyleSheet("QStackedWidget { background-color: #fbfcff; }")
    sys.exit(app.exec())