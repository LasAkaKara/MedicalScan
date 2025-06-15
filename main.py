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
from views.screens.python.prescription_confirm_screen import PrescriptionConfirmScreen

class MedicalApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.current_user_email = None
        self.current_user_id = None
        self.previous_screen = None
        self.stack = QStackedWidget()
        
        # Timer for checking alarms and cleanup
        self.alarm_timer = QTimer(self)
        self.alarm_timer.timeout.connect(self.check_alarm_times)
        self.alarm_timer.start(1000)
        self.last_alarm_times = set()
        
        # Timer for daily cleanup (check every hour)
        self.cleanup_timer = QTimer(self)
        self.cleanup_timer.timeout.connect(self.daily_cleanup_check)
        self.cleanup_timer.start(3600000)  # 1 hour in milliseconds
        self.last_cleanup_date = None

        # Instantiate screens
        self.login_screen = LoginScreen()
        self.signup_screen = SignupScreen()
        self.home_screen = HomeScreen()
        self.verification_screen = VerificationScreen()
        self.reset_password_screen = ResetPasswordScreen()
        self.scan_screen = ScanScreen(app=self)
        self.prescription_screen = PrescriptionScreen(app=self)
        self.profile_screen = ProfileScreen(app=self)
        self.settings_screen = SettingsScreen(app=self)
        self.prescription_detail_screen = PrescriptionDetailScreen()
        self.calendar_screen = CalendarScreen(app=self)
        self.add_prescription_screen = AddPrescriptionScreen()
        self.notification_screen = NotificationScreen(app=self)
        self.prescription_confirm_screen = PrescriptionConfirmScreen(self)

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
        self.stack.addWidget(self.prescription_confirm_screen)


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

        # Connect scan screen to confirmation screen
        self.scan_screen.go_to_confirm.connect(self.show_prescription_confirm)

        # Connect confirmation screen navigation
        self.prescription_confirm_screen.go_back_to_scan.connect(self.show_scan)
        self.prescription_confirm_screen.go_to_prescription.connect(self.show_prescription)

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
            user = self.login_screen.auth_controller.db_service.get_user_by_email(email)
            if user:
                self.current_user_id = user.get("id")
                # Load preferences for timer logic
                self.current_user_prefs = {}
                if user.get("preferences"):
                    try:
                        self.current_user_prefs = json.loads(user["preferences"])
                    except Exception:
                        self.current_user_prefs = {}
                # --- Ensure notification_times is set ---
                if "notification_times" not in self.current_user_prefs:
                    self.current_user_prefs["notification_times"] = {
                        "Sáng": "07:00",
                        "Trưa": "12:00",
                        "Tối": "19:00"
                    }
                    # Save back to DB
                    self.login_screen.auth_controller.db_service.update_user_preferences(
                        user["id"], json.dumps(self.current_user_prefs, ensure_ascii=False)
                    )
                # --- Generate all missed notifications up to now ---
                notif_times = self.current_user_prefs["notification_times"]
                due_labels = self.get_due_time_labels(notif_times)
                for time_label in due_labels:
                    self.settings_screen.db.generate_notification_for_time(self.current_user_id, time_label)
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
        prefs = getattr(self, "current_user_prefs", {})
        if user.get("preferences"):
            try:
                prefs = json.loads(user["preferences"])
            except Exception:
                prefs = {}
        # Default notification times if not set
        notif_times = prefs.get("notification_times", {
            "Sáng": "07:00",
            "Trưa": "12:00",
            "Tối": "19:00"
        })

        def normalize_time(t):
            if isinstance(t, str):
                parts = t.split(":")
                if len(parts) == 2:
                    return f"{int(parts[0]):02d}:{int(parts[1]):02d}"
            return t

        # Always get the current time and date freshly
        now_time = QTime.currentTime().toString("HH:mm")
        now_time = normalize_time(now_time)
        now_date = QDate.currentDate().toString("yyyy-MM-dd")

        # Get switches state from profile screen (if loaded)
        med_on = prefs.get("notify_medication", True)
        refill_on = prefs.get("notify_refills", True)


        # Medicine alarm
        if med_on:
            for time_label in ["Sáng", "Trưa", "Tối"]:
                alarm_time = normalize_time(notif_times.get(time_label))
                alarm_key = (time_label, now_date, now_time)
                if alarm_time and now_time == alarm_time and alarm_key not in self.last_alarm_times:
                    self.settings_screen.db.generate_notification_for_time(self.current_user_id, time_label)
                    self.show_alarm_overlay(f"Đã đến giờ uống thuốc ({time_label.lower()}) rồi")
                    self.last_alarm_times.add(alarm_key)

        self.last_alarm_times = {(k, d, v) for (k, d, v) in self.last_alarm_times if d == now_date and v == now_time}

    def show_alarm_overlay(self, message):
        overlay = AlarmOverlay(message, parent=self.stack)
        overlay.exec()
    
    def get_due_time_labels(self, notif_times):
        now = QTime.currentTime()
        due_labels = []
        for time_label in ["Sáng", "Trưa", "Tối"]:
            alarm_str = notif_times.get(time_label)
            if not alarm_str:
                continue
            alarm_qt = QTime.fromString(alarm_str, "HH:mm")
            if alarm_qt.isValid() and alarm_qt <= now:
                due_labels.append(time_label)
        return due_labels

    def daily_cleanup_check(self):
        """Check if we need to run daily cleanup (mark missed notifications)"""
        current_date = QDate.currentDate().toPython()
        
        # Run cleanup once per day
        if self.last_cleanup_date != current_date:
            self.last_cleanup_date = current_date
            
            # Mark missed notifications from previous days
            if hasattr(self, 'settings_screen') and self.settings_screen.db:
                self.settings_screen.db.mark_missed_notifications()
                print(f"Daily cleanup completed for {current_date}")

    def show_prescription_confirm(self, prescription_data):
        """Show prescription confirmation screen with data"""
        self.prescription_confirm_screen.set_prescription_data(prescription_data)
        self.stack.setCurrentWidget(self.prescription_confirm_screen)

if __name__ == '__main__':
    app = MedicalApp(sys.argv)

    app.setStyleSheet("QStackedWidget { background-color: #fbfcff; }")
    sys.exit(app.exec())