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
        
        # Set the tick handler for the UI
        self.tick_handler = self.handle_tick

    def load_notifications_for_today(self):
        """Load notifications for today and mark any missed ones from previous days"""
        # First, mark any missed notifications from previous days
        self.db.mark_missed_notifications()
        
        # Then load today's notifications
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
        """Handle when user ticks/unticks a notification"""
        notification_id = notification["id"]
        
        if checked:
            # Mark as taken
            success = self.db.mark_notification_taken(notification_id)
            if success:
                notification["taken"] = True
                notification["status"] = "taken"
                print(f"Marked notification {notification_id} as taken")
        else:
            # Mark as not taken (undo)
            success = self.db.mark_notification_untaken(notification_id)
            if success:
                notification["taken"] = False
                notification["status"] = "pending"
                print(f"Marked notification {notification_id} as pending")
        
        # Refresh the display
        self.apply_filter()

    def handle_back(self):
        self.go_back.emit()