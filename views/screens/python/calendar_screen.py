from PySide6.QtCore import Signal
from views.screens.pyside.calendar_screen_ui import CalendarScreenUI
from PySide6.QtCore import QDate

class CalendarScreen(CalendarScreenUI):
    go_to_home = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.back_btn.clicked.connect(self.handle_back)
        self.prev_month_btn.clicked.connect(self.handle_prev_month)
        self.next_month_btn.clicked.connect(self.handle_next_month)
        self.set_month(self.current_year, self.current_month)

    def handle_back(self):
        self.go_to_home.emit()

    def handle_prev_month(self):
        month = self.current_month - 1
        year = self.current_year
        if month < 1:
            month = 12
            year -= 1
        self.set_month(year, month)

    def handle_next_month(self):
        month = self.current_month + 1
        year = self.current_year
        if month > 12:
            month = 1
            year += 1
        self.set_month(year, month)