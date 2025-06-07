from PySide6.QtCore import Signal
from views.screens.pyside.notification_screen_ui import NotificationScreenUI

class NotificationScreen(NotificationScreenUI):
    go_back = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.back_btn.clicked.connect(self.handle_back)
        # Example notifications for today
        self.notifications = [
            {
                "id": 1,
                "title": "Metformin Hydrochloride",
                "subtitle": "08:00 - Sáng: 1 viên",
                "taken": False,
            },
            {
                "id": 2,
                "title": "Fexofenadine Hydrochloride",
                "subtitle": "12:00 - Trưa: 1 viên",
                "taken": True,
            },
            {
                "id": 3,
                "title": "Tamsulosin Hydrochloride",
                "subtitle": "18:00 - Tối: 1 viên",
                "taken": False,
            },
        ]
        self.set_notifications(self.notifications)
        # Connect tick events
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if hasattr(widget, "ticked"):
                widget.ticked.connect(self.handle_tick)

    def handle_tick(self, notification, checked):
        # Store tick in history (implement DB logic here)
        notification["taken"] = checked
        print(f"User {'took' if checked else 'unticked'}: {notification['title']} at {notification['subtitle']}")

    def handle_back(self):
        self.go_back.emit()