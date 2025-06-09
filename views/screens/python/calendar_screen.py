from views.screens.pyside.calendar_screen_ui import CalendarScreenUI
from PySide6.QtCore import QDate, Signal
from services.database_service import DatabaseService
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout
from datetime import datetime, timedelta
import json
from themes import FONT_FAMILY, FONT_SIZE_LG

class CalendarScreen(CalendarScreenUI):
    go_to_home = Signal()
    go_to_notification = Signal()

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.db = DatabaseService()
        self.selected_date = QDate.currentDate()
        self.back_btn.clicked.connect(self.handle_back)
        self.prev_month_btn.clicked.connect(self.handle_prev_month)
        self.next_month_btn.clicked.connect(self.handle_next_month)
        self.bell_btn.clicked.connect(self.go_to_notification.emit)
        self.set_month(self.selected_date.year(), self.selected_date.month())
        self.load_prescriptions_for_date(self.selected_date)

    def load_prescriptions_for_date(self, date: QDate):
        # Clear old widgets
        for i in reversed(range(self.prescription_list_layout.count())):
            widget = self.prescription_list_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        user_id = self.app.current_user_id
        if not user_id:
            return

        prescriptions = self.db.get_user_prescriptions(user_id)
        found = False
        selected_date = date.toPython()

        for p in prescriptions:
            created_at = p.get("created_at")
            if not created_at:
                print(f"created_at missing for prescription: {p.get('name', '')}")
                continue
            created_at = str(created_at).strip()
            created_date = None
            # Try parsing with and without microseconds
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
                try:
                    created_date = datetime.strptime(created_at, fmt).date()
                    break
                except Exception:
                    continue
            if not created_date:
                print(f"Could not parse created_at: {created_at}")
                continue

            medicine_details = p.get("medicine_details", {})
            if isinstance(medicine_details, str):
                try:
                    medicine_details = json.loads(medicine_details)
                except Exception:
                    medicine_details = {}

            duration_days = 1
            medicines = medicine_details.get("medicines", [])
            durations = []
            for med in medicines:
                d = med.get("duration_days", "1")
                if isinstance(d, str):
                    d = ''.join(filter(str.isdigit, d)) or "1"
                try:
                    durations.append(int(d))
                except Exception:
                    durations.append(1)
            if durations:
                duration_days = max(durations)

            
            if created_date <= selected_date < created_date + timedelta(days=duration_days):
                found = True
                card = QFrame()
                card.setStyleSheet("background: #fafdff; border-radius: 12px; border: 1px solid #e0e0e0;")
                layout = QVBoxLayout(card)
                name = QLabel(f"Đơn: {p.get('name', '')}")
                name.setStyleSheet("font-size: 15px; font-weight: bold; color: #406D96; border: none;")
                layout.addWidget(name)
                hospital = QLabel(f"Bệnh viện: {p.get('hospital_name', '')}")
                hospital.setStyleSheet("border: none;")
                layout.addWidget(hospital)
                created_label = QLabel(f"Ngày tạo: {created_at}")
                created_label.setStyleSheet("border: none;")
                layout.addWidget(created_label)
                self.prescription_list_layout.addWidget(card)

        if not found:
            self.prescription_list_layout.addWidget(QLabel("Không có đơn thuốc nào cho ngày này."))
    
    def _on_date_clicked(self, day):
        self.selected_date = QDate(self.current_year, self.current_month, day)
        self._draw_calendar()
        self.load_prescriptions_for_date(self.selected_date)
    
    def set_month(self, year, month):
        self.current_year = year
        self.current_month = month
        self.month_label.setText(f"{month:02d}/{year}")
        self.month_label.setStyleSheet(f"font-weight: 600; color: #406D96; font-family: {FONT_FAMILY}; font-size: {FONT_SIZE_LG}px; border: none;")
        self._draw_calendar()

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