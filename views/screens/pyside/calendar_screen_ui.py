from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QSizePolicy, QToolButton, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QIcon, QColor, QFont
from themes import FONT_SIZE_MD, FONT_SIZE_LG, FONT_SIZE_XL, PRIMARY_COLOR, FONT_FAMILY, TEXT_COLOR, HINT_COLOR

DAYS = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]  # Monday to Sunday

class CalendarScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_date = QDate.currentDate()
        self.current_month = self.selected_date.month()
        self.current_year = self.selected_date.year()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 0, 24, 0)
        main_layout.setSpacing(0)

        # --- Header ---
        header = QHBoxLayout()
        header.setContentsMargins(16, 16, 16, 0)
        header.setSpacing(0)

        # Back button
        self.back_btn = QToolButton()
        self.back_btn.setIcon(QIcon("assets/back.png"))
        self.back_btn.setIconSize(QSize(28, 28))
        self.back_btn.setStyleSheet("background: transparent;")
        header.addWidget(self.back_btn, alignment=Qt.AlignLeft)

        # Center title/subtitle
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        center_layout.setAlignment(Qt.AlignCenter)
        self.title_label = QLabel("Lịch thuốc")
        self.title_label.setStyleSheet(f"font-size: {FONT_SIZE_LG}px; font-weight: bold; color: {PRIMARY_COLOR};")
        self.title_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.title_label)
        self.subtitle_label = QLabel("Xem lịch uống thuốc của bạn tại đây")
        self.subtitle_label.setStyleSheet("font-size: 13px; color: #667085;")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.subtitle_label)
        header.addWidget(center_widget, stretch=1)

        # Bell icon
        self.bell_btn = QToolButton()
        self.bell_btn.setIcon(QIcon("assets/bell.png"))
        self.bell_btn.setIconSize(QSize(28, 28))
        self.bell_btn.setStyleSheet("background: transparent;")
        header.addWidget(self.bell_btn, alignment=Qt.AlignRight)

        main_layout.addLayout(header)
        main_layout.addSpacing(24)

        # --- Month Navigation ---
        month_card = QFrame()
        month_card.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 14px;
                border: 1px solid #e0e0e0;
            }
        """)
        month_shadow = QGraphicsDropShadowEffect(self)
        month_shadow.setBlurRadius(10)
        month_shadow.setOffset(0, 2)
        month_shadow.setColor(Qt.gray)
        month_card.setGraphicsEffect(month_shadow)

        month_nav = QHBoxLayout(month_card)
        month_nav.setContentsMargins(18, 8, 18, 8)  # Padding inside the card
        month_nav.setSpacing(8)

        self.prev_month_btn = QToolButton()
        self.prev_month_btn.setIcon(QIcon("assets/arrow-left.png"))
        self.prev_month_btn.setIconSize(QSize(24, 24))
        self.prev_month_btn.setStyleSheet("background: transparent;")
        month_nav.addWidget(self.prev_month_btn)

        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; min-width: 120px; border: none;")
        month_nav.addWidget(self.month_label, stretch=1)

        self.next_month_btn = QToolButton()
        self.next_month_btn.setIcon(QIcon("assets/arrow-right.png"))
        self.next_month_btn.setIconSize(QSize(24, 24))
        self.next_month_btn.setStyleSheet("background: transparent;")
        month_nav.addWidget(self.next_month_btn)

        main_layout.addWidget(month_card)
        main_layout.addSpacing(16)

        # --- Calendar Grid ---
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setContentsMargins(24, 12, 24, 12)
        self.calendar_grid.setSpacing(10)
        calendar_card = QFrame()
        calendar_card.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 18px;
                border: 1px solid #e0e0e0;
                font-family: 'Roboto', sans-serif;
            }
        """)
        calendar_shadow = QGraphicsDropShadowEffect(self)
        calendar_shadow.setBlurRadius(16)
        calendar_shadow.setOffset(0, 4)
        calendar_shadow.setColor(Qt.gray)
        calendar_card.setGraphicsEffect(calendar_shadow)

        calendar_card_layout = QVBoxLayout(calendar_card)
        calendar_card_layout.setContentsMargins(0, 0, 0, 0)
        calendar_card_layout.setSpacing(0)
        calendar_card_layout.addLayout(self.calendar_grid)

        main_layout.addWidget(calendar_card)
        main_layout.setAlignment(Qt.AlignTop)

        self._draw_calendar()

    def _draw_calendar(self):
        # Clear grid
        for i in reversed(range(self.calendar_grid.count())):
            widget = self.calendar_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Days of week header
        for i, day in enumerate(DAYS):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; font-weight: bold; color: {TEXT_COLOR}; border: none;")
            self.calendar_grid.addWidget(lbl, 0, i)

        # Dates
        first_day = QDate(self.current_year, self.current_month, 1)
        start_col = (first_day.dayOfWeek() + 5) % 7  # Monday=0, Sunday=6
        days_in_month = first_day.daysInMonth()
        row = 1
        col = start_col
        today = QDate.currentDate()
        self.date_buttons = []

        for day in range(1, days_in_month + 1):
            btn = QPushButton(str(day))
            btn.setCheckable(True)
            btn.setFixedSize(36, 36)
            btn.setStyleSheet(self._date_btn_style(day, today))
            btn.clicked.connect(lambda checked, d=day: self._on_date_clicked(d))
            self.date_buttons.append(btn)
            self.calendar_grid.addWidget(btn, row, col)
            # Highlight today or selected
            if (self.selected_date.year() == self.current_year and
                self.selected_date.month() == self.current_month and
                self.selected_date.day() == day):
                btn.setChecked(True)
            col += 1
            if col > 6:
                col = 0
                row += 1

    def _date_btn_style(self, day, today):
        # Style for normal, today, and selected
        base = """
            QPushButton {
                border-radius: 18px;
                font-size: 15px;
                color: #666666;
                border: none;
            }
            QPushButton:checked {
                background: #406D96;
                color: #fff;
                font-weight: bold;
            }
        """
        if (self.current_year == today.year() and
            self.current_month == today.month() and
            today.day() == day):
            base += """
                QPushButton {
                    border: 2px solid #43a047;
                }
            """
        return base

    def _on_date_clicked(self, day):
        self.selected_date = QDate(self.current_year, self.current_month, day)
        self._draw_calendar()

    def set_month(self, year, month):
        self.current_year = year
        self.current_month = month
        self.month_label.setText(f"{month:02d}/{year}")
        self.month_label.setStyleSheet(f"font-weight: 600; color: {PRIMARY_COLOR}; font-family: {FONT_FAMILY}; font-size: {FONT_SIZE_LG}px; border: none;")
        self._draw_calendar()