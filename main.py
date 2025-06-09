import sys
import json
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QIcon
from views.components.alarm_overlay import AlarmOverlay
from PySide6.QtCore import QTimer, QTime, QDate
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
from views.screens.python.calendar_screen import CalendarScreen
from views.screens.python.add_prescription_screen import AddPrescriptionScreen
from views.screens.python.notification_screen import NotificationScreen

class MedicalApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.current_user_email = None
        self.current_user_id = None
        self.previous_screen = None
        self.stack = QStackedWidget()
        self.alarm_timer = QTimer(self)
        self.alarm_timer.timeout.connect(self.check_alarm_times)
        self.alarm_timer.start(1000)
        self.last_alarm_times = set()

        # Instantiate screens
        self.login_screen = LoginScreen()
        self.signup_screen = SignupScreen()
        self.home_screen = HomeScreen()
        self.verification_screen = VerificationScreen()
        self.reset_password_screen = ResetPasswordScreen()
        self.scan_screen = ScanScreen()
        self.prescription_screen = PrescriptionScreen(app=self)
        self.profile_screen = ProfileScreen(app=self)
        self.settings_screen = SettingsScreen(app=self)
        self.prescription_detail_screen = PrescriptionDetailScreen()
        self.calendar_screen = CalendarScreen(app=self)
        self.add_prescription_screen = AddPrescriptionScreen()
        self.notification_screen = NotificationScreen(app=self)

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
        self.stack.addWidget(self.prescription_detail_screen)
        self.stack.addWidget(self.calendar_screen)
        self.stack.addWidget(self.add_prescription_screen)
        self.stack.addWidget(self.notification_screen)


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
        self.prescription_screen.go_to_notification.connect(self.show_notification)
        self.profile_screen.go_to_login.connect(self.show_login)
        self.profile_screen.go_to_home.connect(self.show_home)
        self.settings_screen.go_to_home.connect(self.show_home)
        self.prescription_detail_screen.go_to_history.connect(self.show_prescription)
        self.home_screen.go_to_calendar.connect(self.show_calendar)
        self.calendar_screen.go_to_home.connect(self.show_home)
        self.calendar_screen.go_to_notification.connect(self.show_notification)
        self.prescription_screen.go_to_add_prescription.connect(self.show_add_prescription)
        self.prescription_screen.go_to_scan.connect(self.show_scan)
        self.prescription_screen.go_to_detail.connect(self.show_prescription_detail)
        self.add_prescription_screen.go_to_prescription.connect(self.show_prescription)
        self.notification_screen.go_back.connect(self.handle_notification_back)
        self.home_screen.go_to_notification.connect(self.show_notification)



        # Verification navigation
        self.login_screen.go_to_verify.connect(self.show_verification)
        self.signup_screen.go_to_verify.connect(self.show_verification)
        self.verification_screen.go_to_login.connect(self.show_login)

        # Reset password navigation
        self.login_screen.go_to_reset_password.connect(self.show_reset_password)
        self.reset_password_screen.go_to_login.connect(self.show_login)


        # Set window title and icon
        self.stack.setWindowTitle("MedicalScan")
        self.stack.setWindowIcon(QIcon("assets/app-logo.png"))
        self.stack.setCurrentWidget(self.login_screen)
        self.stack.setFixedSize(400, 700)
        self.stack.show()

    def show_signup(self):
        self.stack.setCurrentWidget(self.signup_screen)

    def show_login(self):
        self.current_user_email = None
        self.stack.setCurrentWidget(self.login_screen)

    def show_home(self, email=None):
        if email:
            self.current_user_email = email
            # Fetch user_id from DB
            user = self.login_screen.auth_controller.db_service.get_user_by_email(email)
            if user:
                self.current_user_id = user.get("id")
        self.home_screen.set_user(self.current_user_email)
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
        self.prescription_screen.load_prescriptions(self.current_user_id)
        self.stack.setCurrentWidget(self.prescription_screen)

    def show_add_prescription(self):
        # Implement this to show your add prescription screen
        pass

    def show_profile(self):
        self.profile_screen.load_user_data(self.current_user_email)
        self.stack.setCurrentWidget(self.profile_screen)
    
    def show_settings(self):
        self.settings_screen.load_settings()
        self.stack.setCurrentWidget(self.settings_screen)
    
    def show_prescription_detail(self, prescription_id):
        self.prescription_detail_screen.set_prescription_id(prescription_id)
        self.stack.setCurrentWidget(self.prescription_detail_screen)
    
    def show_calendar(self):
        self.calendar_screen.selected_date = QDate.currentDate()
        self.calendar_screen.set_month(
            self.calendar_screen.selected_date.year(),
            self.calendar_screen.selected_date.month()
        )
        self.calendar_screen._draw_calendar() 
        self.calendar_screen.load_prescriptions_for_date(self.calendar_screen.selected_date)
        self.stack.setCurrentWidget(self.calendar_screen)

    def show_add_prescription(self):
        self.stack.setCurrentWidget(self.add_prescription_screen)
    
    def show_prescription_detail(self, prescription):
        self.prescription_detail_screen.set_prescription(prescription)
        self.stack.setCurrentWidget(self.prescription_detail_screen)
    
    def show_notification(self):
        # Store the current screen before switching
        self.previous_screen = self.stack.currentWidget()
        self.notification_screen.load_notifications_for_today()
        self.stack.setCurrentWidget(self.notification_screen)

    def handle_notification_back(self):
        # Go back to the previous screen if set, else home
        if self.previous_screen is not None:
            self.stack.setCurrentWidget(self.previous_screen)
            self.previous_screen = None
        else:
            self.stack.setCurrentWidget(self.home_screen)

    def check_alarm_times(self):
        # Only check if user is logged in
        if not self.current_user_id:
            return
        user = self.settings_screen.db.get_user_by_id(self.current_user_id)
        if not user:
            return
        prefs = {}
        if user.get("preferences"):
            try:
                prefs = json.loads(user["preferences"])
            except Exception:
                prefs = {}
        notif_times = prefs.get("notification_times", {})

        # Always get the current time and date freshly
        now_time = QTime.currentTime().toString("HH:mm")
        now_date = QDate.currentDate().toString("yyyy-MM-dd")

        # Get switches state from profile screen (if loaded)
        med_on = getattr(self.profile_screen, "notif_medication", None)
        refill_on = getattr(self.profile_screen, "notif_refills", None)
        med_on = med_on.isChecked() if med_on is not None else True
        refill_on = refill_on.isChecked() if refill_on is not None else True

        # Medicine alarm
        if med_on:
            for t in ["morning", "noon", "evening"]:
                alarm_time = notif_times.get(t)
                # Use both time and date as key to avoid duplicate alarms after midnight
                alarm_key = (t, now_date, now_time)
                if alarm_time and now_time == alarm_time and alarm_key not in self.last_alarm_times:
                    self.last_alarm_times.add(alarm_key)
                    self.show_alarm_overlay("Đã đến giờ uống thuốc rồi")
        # Clean up old times (keep only current date)
        self.last_alarm_times = {(k, d, v) for (k, d, v) in self.last_alarm_times if d == now_date and v == now_time}

    def show_alarm_overlay(self, message):
        overlay = AlarmOverlay(message, parent=self.stack)
        overlay.exec()



if __name__ == '__main__':
    app = MedicalApp(sys.argv)

    app.setStyleSheet("QStackedWidget { background-color: #fbfcff; }")
    sys.exit(app.exec())