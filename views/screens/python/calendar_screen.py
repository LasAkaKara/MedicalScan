from views.screens.pyside.calendar_screen_ui import CalendarScreenUI
from PySide6.QtCore import QDate, Signal
from services.database_service import DatabaseService
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout
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

        # Get notification statuses for this date
        notification_statuses = self.db.get_all_notification_statuses_for_date(user_id, selected_date)

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
                prescription_id = p.get("id")
                
                # Group medicines by time
                for med in medicines:
                    usage_times = med.get("usage_time", [])
                    # Handle both ["Sáng", "Tối"] and [{"time": "Sáng", ...}]
                    if usage_times and isinstance(usage_times[0], dict):
                        for t in usage_times:
                            label = t.get("time", "")
                            if label in time_groups:
                                # Check notification status for this medicine time
                                status_key = (prescription_id, label)
                                status = notification_statuses.get(status_key, 'none')
                                
                                time_groups[label].append({
                                    "name": med.get("medicine_name", ""),
                                    "status": status,
                                    "prescription_id": prescription_id
                                })
                    else:
                        for label in usage_times:
                            if label in time_groups:
                                # Check notification status for this medicine time
                                status_key = (prescription_id, label)
                                status = notification_statuses.get(status_key, 'none')
                                
                                time_groups[label].append({
                                    "name": med.get("medicine_name", ""),
                                    "status": status,
                                    "prescription_id": prescription_id
                                })

        # Display grouped medicines with status overlays
        if found:
            for time_label in ["Sáng", "Trưa", "Tối"]:
                meds = time_groups[time_label]
                if meds:
                    card = self.create_medicine_time_card(time_label, meds, selected_date)
                    self.prescription_list_layout.addWidget(card)
        else:
            no_prescription_label = QLabel("Không có đơn thuốc nào cho ngày này.")
            no_prescription_label.setStyleSheet("font-size: 15px; color: #666; text-align: center; padding: 20px;")
            self.prescription_list_layout.addWidget(no_prescription_label)

    def create_medicine_time_card(self, time_label, medicines, selected_date):
        """Create a card for medicines at a specific time with status overlay"""
        card = QFrame()
        
        # Determine overall status for this time slot
        statuses = [med["status"] for med in medicines]
        if all(status == "taken" for status in statuses):
            overall_status = "taken"
            card_color = "#f0f9ff"  # Light blue for taken
            border_color = "#22c55e"  # Green border
        elif any(status == "missed" for status in statuses):
            overall_status = "missed"
            card_color = "#fef2f2"  # Light red for missed
            border_color = "#ef4444"  # Red border
        elif selected_date < datetime.now().date() and any(status == "pending" for status in statuses):
            overall_status = "missed"
            card_color = "#fef2f2"  # Light red for missed
            border_color = "#ef4444"  # Red border
        else:
            overall_status = "pending"
            card_color = "#fafdff"  # Default light color
            border_color = "#e0e0e0"  # Default border
        
        card.setStyleSheet(f"""
            QFrame {{
                background: {card_color};
                border-radius: 12px;
                border: 2px solid {border_color};
                margin-bottom: 8px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        
        # Header with time and status overlay
        header_layout = QHBoxLayout()
        
        time_lbl = QLabel(f"<b>{time_label}</b>")
        time_lbl.setStyleSheet("font-size: 16px; color: #406D96; border: none;")
        header_layout.addWidget(time_lbl)
        
        header_layout.addStretch()
        
        # Status overlay
        if overall_status == "taken":
            status_overlay = QLabel("✔ Đã uống")
            status_overlay.setStyleSheet("""
                background: #22c55e;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            """)
        elif overall_status == "missed":
            status_overlay = QLabel("✗ Chưa uống")
            status_overlay.setStyleSheet("""
                background: #ef4444;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            """)
        else:
            status_overlay = QLabel("⏳ Chờ uống")
            status_overlay.setStyleSheet("""
                background: #f59e0b;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            """)
        
        header_layout.addWidget(status_overlay)
        layout.addLayout(header_layout)
        
        # Medicine list
        for med in medicines:
            name = med["name"]
            med_status = med["status"]
            
            med_layout = QHBoxLayout()
            
            # Medicine name
            med_lbl = QLabel(f"• {name}")
            if med_status == "taken":
                med_lbl.setStyleSheet("font-size: 14px; color: #16a34a; border: none; margin-left: 8px;")
            elif med_status == "missed":
                med_lbl.setStyleSheet("font-size: 14px; color: #dc2626; border: none; margin-left: 8px;")
            else:
                med_lbl.setStyleSheet("font-size: 14px; color: #374151; border: none; margin-left: 8px;")
            
            med_layout.addWidget(med_lbl)
            med_layout.addStretch()
            
            # Individual medicine status icon
            if med_status == "taken":
                status_icon = QLabel("✓")
                status_icon.setStyleSheet("color: #16a34a; font-weight: bold; font-size: 14px;")
            elif med_status == "missed":
                status_icon = QLabel("✗")
                status_icon.setStyleSheet("color: #dc2626; font-weight: bold; font-size: 14px;")
            else:
                status_icon = QLabel("○")
                status_icon.setStyleSheet("color: #9ca3af; font-weight: bold; font-size: 14px;")
            
            med_layout.addWidget(status_icon)
            layout.addLayout(med_layout)
        
        return card
    
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
    
    def is_time_taken(self, user_id, prescription_id, time_label, date):
        return self.db.is_time_taken(user_id, prescription_id, time_label, date)