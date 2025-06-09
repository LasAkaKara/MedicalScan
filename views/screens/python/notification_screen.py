from PySide6.QtCore import Signal
from views.screens.pyside.notification_screen_ui import NotificationScreenUI
from services.database_service import DatabaseService
from datetime import datetime, timedelta
import json

class NotificationScreen(NotificationScreenUI):
    go_back = Signal()

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.back_btn.clicked.connect(self.handle_back)
        self.db = DatabaseService()

        # Connect filter buttons
        self.filter_group.buttonClicked.connect(self.apply_filter)

        self.all_notifications = []
        self.filtered_notifications = []
        self.current_filter = "Tất cả"


    
    def load_notifications_for_today(self):
        today = datetime.now().date()
        user_id = self.app.current_user_id
        prescriptions = self.db.get_user_prescriptions(user_id)
        notifications = []
        for presc in prescriptions:
            presc_name = presc.get("name", "")
            medicine_details = presc.get("medicine_details", {})
            if isinstance(medicine_details, str):
                try:
                    medicine_details = json.loads(medicine_details)
                except Exception:
                    medicine_details = {}
            for med in medicine_details.get("medicines", []):
                med_name = med.get("medicine_name", "")
                usage_times = med.get("usage_time", [])
                duration_days = med.get("duration_days", "1")
                try:
                    duration_days = int(duration_days)
                except Exception:
                    duration_days = 1
                # Assume prescription created_at is the start date
                start_date = presc.get("created_at")
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").date()
                    except Exception:
                        start_date = today
                elif isinstance(start_date, datetime):
                    start_date = start_date.date()
                else:
                    start_date = today
                # For each day in duration, if today matches, create notifications for each usage_time
                for day_offset in range(duration_days):
                    dose_date = start_date + timedelta(days=day_offset)
                    if dose_date == today:
                        for t in usage_times:
                            # t can be dict or str
                            if isinstance(t, dict):
                                time_label = t.get("time", "")
                                quantity = t.get("quantity", 1)
                            else:
                                time_label = t
                                quantity = med.get("quantity_per_time", 1)
                            notifications.append({
                                "prescription_name": presc_name,
                                "medicine_name": med_name,
                                "time": time_label,
                                "subtitle": f"{time_label}: {quantity} viên",
                                "taken": False,  # You can load this from DB/history if implemented
                            })
        self.all_notifications = notifications
        self.apply_filter()  # Show all by default

    def apply_filter(self):
        # Get selected filter
        checked_btn = self.filter_group.checkedButton()
        if checked_btn:
            self.current_filter = checked_btn.text()
        if self.current_filter == "Tất cả":
            self.filtered_notifications = self.all_notifications
        else:
            self.filtered_notifications = [
                n for n in self.all_notifications if n.get("time", "") == self.current_filter
            ]
        self.set_notifications(self.filtered_notifications)

    def handle_tick(self, notification, checked):
        # Store tick in history (implement DB logic here)
        notification["taken"] = checked
        print(f"User {'took' if checked else 'unticked'}: {notification['title']} at {notification['subtitle']}")

    def handle_back(self):
        self.go_back.emit()