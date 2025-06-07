from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QScrollArea, QCheckBox
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QFont

class NotificationItem(QFrame):
    ticked = Signal(dict, bool)  # (notification, checked)

    def __init__(self, notification, parent=None):
        super().__init__(parent)
        self.notification = notification
        self.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
                margin-bottom: 10px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        # Info
        info_layout = QVBoxLayout()
        title = QLabel(notification.get("title", ""))
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

        # Scroll area for notifications
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
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
            # You can connect item.ticked to a handler in your logic class