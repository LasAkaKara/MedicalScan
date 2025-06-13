from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QScrollArea,
    QCheckBox, QButtonGroup, QButtonGroup, QRadioButton, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QFont, QColor, QPainter, QPen, QBrush
from themes import FONT_SIZE_MD, FONT_SIZE_LG, PRIMARY_COLOR, TEXT_COLOR, HINT_COLOR

class ConfirmButton(QPushButton):
    """Custom confirmation button for medicine intake"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_confirmed = False
        self.setText("Xác nhận đã uống")
        self.setCheckable(True)
        self.setFixedHeight(40)
        self.setMinimumWidth(140)
        self.update_style()
        
    def update_style(self):
        if self.is_confirmed:
            self.setStyleSheet("""
                QPushButton {
                    background: #22c55e;
                    color: white;
                    border: 2px solid #22c55e;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: bold;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background: #16a34a;
                    border-color: #16a34a;
                }
                QPushButton:pressed {
                    background: #15803d;
                }
            """)
            self.setText("Đã uống")
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: #ffffff;
                    color: #406D96;
                    border: 2px solid #406D96;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: bold;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background: #f0f9ff;
                    border-color: #2563eb;
                    color: #2563eb;
                }
                QPushButton:pressed {
                    background: #dbeafe;
                }
            """)
            self.setText("Xác nhận đã uống")
    
    def set_confirmed(self, confirmed):
        self.is_confirmed = confirmed
        self.setChecked(confirmed)
        self.update_style()

class CircularCheckBox(QCheckBox):
    """Custom circular checkbox that's bigger and easier to tap"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 60)  # Make it bigger for easier tapping
        self.setStyleSheet("""
            QCheckBox {
                background: transparent;
                border: none;
            }
            QCheckBox::indicator {
                width: 0px;
                height: 0px;
                background: transparent;
                border: none;
            }
        """)
    
class NotificationItem(QFrame):
    ticked = Signal(dict, bool)  # (notification, checked)

    def __init__(self, notification, tick_handler=None, parent=None):
        super().__init__(parent)
        self.notification = notification
        self.tick_handler = tick_handler  # Store the handler function
        self.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 14px;
                margin-bottom: 10px;
                font-family: 'Roboto', sans-serif;
            }
        """)
        # Add shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(12)

        # Top section with prescription info
        top_layout = QHBoxLayout()
        top_layout.setSpacing(12)

        # Info section
        info_layout = QVBoxLayout()
        presc_label = QLabel(f"{notification.get('prescription_name', '')}")
        presc_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; font-weight: bold; color: {PRIMARY_COLOR};")
        info_layout.addWidget(presc_label)

        # Medicine time label
        time_label = QLabel(f"{notification.get('time', '')}:")
        time_label.setStyleSheet(f"font-size: 15px; color: #406D96; font-weight: bold;")
        info_layout.addWidget(time_label)

        # List medicines vertically
        for med in notification.get("medicines", []):
            name = med.get("medicine_name", "")
            qty = med.get("quantity_per_time", "")
            med_lbl = QLabel(f"{name} ({qty})" if qty else f"{name}")
            med_lbl.setStyleSheet("font-size: 14px; color: #374151; margin-left: 8px;")
            med_lbl.setWordWrap(True)  # Allow text wrapping for long medicine names
            info_layout.addWidget(med_lbl)
            
        top_layout.addLayout(info_layout)
        main_layout.addLayout(top_layout)

        # Bottom section with confirmation button
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push button to the right

        # Check the status from the notification
        is_taken = notification.get("taken", False) or notification.get("status") == "taken"

        # Confirmation button
        self.confirm_btn = ConfirmButton()
        self.confirm_btn.set_confirmed(is_taken)
        self.confirm_btn.clicked.connect(self.on_confirm_clicked)
        
        button_layout.addWidget(self.confirm_btn)
        main_layout.addLayout(button_layout)

    def on_confirm_clicked(self):
        # Toggle the confirmation state
        new_state = not self.confirm_btn.is_confirmed
        self.confirm_btn.set_confirmed(new_state)
        
        # Call the handler function directly if provided
        if self.tick_handler:
            self.tick_handler(self.notification, new_state)
        
        # Also emit the signal for any other listeners
        self.ticked.emit(self.notification, new_state)

class NotificationScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông báo")
        self.tick_handler = None  # Will be set by the NotificationScreen
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Top bar
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon("assets/back.png"))
        self.back_btn.setIconSize(QSize(28, 28))
        self.back_btn.setFixedSize(36, 36)
        self.back_btn.setStyleSheet("background: transparent;")
        top_bar.addWidget(self.back_btn)
        title = QLabel("Thông báo thuốc hôm nay")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #002D40;")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # --- Enhanced Filter bar (Segmented style) ---
        filter_row = QHBoxLayout()
        filter_row.setSpacing(0)
        self.filter_group = QButtonGroup(self)
        self.filter_all = QPushButton("Tất cả")
        self.filter_morning = QPushButton("🌅 Sáng")
        self.filter_noon = QPushButton("☀️ Trưa")
        self.filter_evening = QPushButton("🌙 Tối")
        for btn in [self.filter_all, self.filter_morning, self.filter_noon, self.filter_evening]:
            btn.setCheckable(True)
            btn.setMinimumWidth(80)
            btn.setMinimumHeight(40)  # Make filter buttons taller for easier tapping
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: #e3eaf6;
                    color: #406D96;
                    font-weight: bold;
                    padding: 10px 8px;
                    border-radius: 0;
                    font-size: 14px;
                }
                QPushButton:checked {
                    background: #406D96;
                    color: #fff;
                }
                QPushButton:hover {
                    background: #d1d9e6;
                }
                QPushButton:checked:hover {
                    background: #2d5a87;
                }
                QPushButton:first-child {
                    border-top-left-radius: 12px;
                    border-bottom-left-radius: 12px;
                }
                QPushButton:last-child {
                    border-top-right-radius: 12px;
                    border-bottom-right-radius: 12px;
                }
            """)
            self.filter_group.addButton(btn)
            filter_row.addWidget(btn)
        self.filter_all.setChecked(True)
        filter_row.addStretch()
        main_layout.addLayout(filter_row)

        # Scroll area for notifications
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollArea > QWidget { background: transparent; }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 4px 2px 4px 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #D0D5DD;
                min-height: 36px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9CA3AF;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
                border: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        main_layout.addWidget(scroll)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(12)  # Increased spacing between notification items
        self.container.setStyleSheet("background: transparent;")
        scroll.setWidget(self.container)

    def set_notifications(self, notifications):
        # Clear old
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Add new
        for notif in notifications:
            item = NotificationItem(notif, tick_handler=self.tick_handler)
            self.layout.addWidget(item)