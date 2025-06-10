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
        notifications = self.db.get_today_notifications(self.app.current_user_id)
        self.all_notifications = notifications
        self.apply_filter()

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
        self.db.mark_notification_taken(notification["id"])
        notification["taken"] = checked
        print(f"User {'took' if checked else 'unticked'}: {notification['title']} at {notification['subtitle']}")

    def handle_back(self):
        self.go_back.emit()