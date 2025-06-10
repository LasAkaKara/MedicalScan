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

        # Group all medicines by time of day
        time_groups = {"Sáng": [], "Trưa": [], "Tối": []}

        for p in prescriptions:
            created_at = p.get("created_at")
            if not created_at:
                continue
            created_at = str(created_at).strip()
            created_date = None
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
                try:
                    created_date = datetime.strptime(created_at, fmt).date()
                    break
                except Exception:
                    continue
            if not created_date:
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
                # Group medicines by time
                for med in medicines:
                    usage_times = med.get("usage_time", [])
                    # Handle both ["Sáng", "Tối"] and [{"time": "Sáng", ...}]
                    if usage_times and isinstance(usage_times[0], dict):
                        for t in usage_times:
                            label = t.get("time", "")
                            if label in time_groups:
                                time_groups[label].append(med.get("medicine_name", ""))
                    else:
                        for label in usage_times:
                            if label in time_groups:
                                time_groups[label].append(med.get("medicine_name", ""))

        # Display grouped medicines
        if found:
            for time_label in ["Sáng", "Trưa", "Tối"]:
                meds = time_groups[time_label]
                if meds:
                    card = QFrame()
                    card.setStyleSheet("background: #fafdff; border-radius: 12px; border: 1px solid #e0e0e0;")
                    layout = QVBoxLayout(card)
                    time_lbl = QLabel(f"<b>{time_label}</b>")
                    time_lbl.setStyleSheet("font-size: 16px; color: #406D96; border: none;")
                    layout.addWidget(time_lbl)
                    for med in medicines:
                        # Check if this medicine is in this time group
                        usage_times = med.get("usage_time", [])
                        # Normalize usage_times to list of strings
                        times = []
                        if usage_times and isinstance(usage_times[0], dict):
                            times = [t.get("time", "") for t in usage_times]
                        else:
                            times = usage_times
                        if time_label in times:
                            name = med.get("medicine_name", "")
                            qty = med.get("quantity_per_time", "")
                            med_lbl = QLabel(f"- {name} ({qty})" if qty else f"- {name}")
                            med_lbl.setStyleSheet("font-size: 15px; color: #222; border: none; margin-left: 8px;")
                            layout.addWidget(med_lbl)
                    self.prescription_list_layout.addWidget(card)
        else:
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