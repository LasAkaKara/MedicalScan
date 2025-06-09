from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QScrollArea,
    QCheckBox, QButtonGroup, QButtonGroup, QRadioButton, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QFont, QColor

class NotificationItem(QFrame):
    ticked = Signal(dict, bool)  # (notification, checked)

    def __init__(self, notification, parent=None):
        super().__init__(parent)
        self.notification = notification
        self.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 14px;
                margin-bottom: 10px;
            }
        """)
        # Add shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        # Info
        info_layout = QVBoxLayout()
        presc_label = QLabel(f"Đơn: {notification.get('prescription_name', '')}")
        presc_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #406D96;")
        info_layout.addWidget(presc_label)
        title = QLabel(notification.get("medicine_name", ""))
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #344054;")
        info_layout.addWidget(title)
        subtitle = QLabel(notification.get("subtitle", ""))
        subtitle.setStyleSheet("font-size: 13px; color: #406D96;")
        info_layout.addWidget(subtitle)
        layout.addLayout(info_layout)

        layout.addStretch()

        # Tick checkbox
        self.tick = QCheckBox()
        self.tick.setChecked(notification.get("taken", False))
        self.tick.setStyleSheet("QCheckBox { font-size: 18px; }")
        self.tick.stateChanged.connect(self.on_tick)
        layout.addWidget(self.tick)

    def on_tick(self, state):
        self.ticked.emit(self.notification, bool(state))

class NotificationScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông báo")
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
        self.filter_morning = QPushButton("Sáng")
        self.filter_noon = QPushButton("Trưa")
        self.filter_evening = QPushButton("Tối")
        for btn in [self.filter_all, self.filter_morning, self.filter_noon, self.filter_evening]:
            btn.setCheckable(True)
            btn.setMinimumWidth(80)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: #e3eaf6;
                    color: #406D96;
                    font-weight: bold;
                    padding: 8px 0;
                    border-radius: 0;
                }
                QPushButton:checked {
                    background: #406D96;
                    color: #fff;
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
                width: 6px;
                margin: 4px 2px 4px 0px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #D0D5DD;
                min-height: 36px;
                border-radius: 3px;
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
        self.layout.setSpacing(8)
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
            item = NotificationItem(notif)
            self.layout.addWidget(item)