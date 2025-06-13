from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QApplication
from PySide6.QtCore import Qt, QTimer, QTime, QUrl
from PySide6.QtGui import QFont, QPainter, QColor
from PySide6.QtMultimedia import QSoundEffect
import os

class AlarmOverlay(QDialog):
    def __init__(self, message="Đã đến giờ uống thuốc rồi", parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Card for alarm content
        card = QWidget(self)
        card.setStyleSheet("""
            background: rgba(255,255,255,0.95);
            border-radius: 24px;
        """)
        card.setMaximumWidth(420)  # Prevent card from overflowing overlay
        card.setMinimumWidth(260)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setContentsMargins(24, 24, 24, 24)

        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 48, QFont.Bold))
        self.time_label.setStyleSheet("color: #222;")
        card_layout.addWidget(self.time_label, alignment=Qt.AlignCenter)

        self.msg_label = QLabel(message)
        self.msg_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.msg_label.setStyleSheet("color: #222; margin-bottom: 24px;")
        card_layout.addWidget(self.msg_label, alignment=Qt.AlignCenter)

        btn_row = QHBoxLayout()
        self.snooze_btn = QPushButton("Snooze")
        self.snooze_btn.setStyleSheet("background: #e0e0e0; color: #2F3A56; border-radius: 8px; padding: 12px 32px; font-size: 18px;")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setStyleSheet("background: #F44336; color: white; border-radius: 8px; padding: 12px 32px; font-size: 18px;")
        btn_row.addWidget(self.snooze_btn)
        btn_row.addWidget(self.stop_btn)
        card_layout.addLayout(btn_row)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(card, alignment=Qt.AlignCenter)

        self.snooze_btn.clicked.connect(self.handle_snooze)
        self.stop_btn.clicked.connect(self.accept)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        self.sound = QSoundEffect(self)
        self.sound.setSource(QUrl.fromLocalFile(os.path.abspath("assets/sounds/alarm_sound.wav")))
        self.sound.setLoopCount(-2)
        self.sound.setVolume(0.8)
        self.sound.play()

        self.snooze_btn.clicked.connect(self.handle_snooze)
        self.stop_btn.clicked.connect(self.accept)


    def showEvent(self, event):
        # Ensure overlay covers the parent widget exactly
        if self.parent():
            self.resize(self.parent().width(), self.parent().height())
            self.move(self.parent().mapToGlobal(self.parent().rect().topLeft()))
        else:
            # fallback: center on primary screen
            screen = self.screen() or QApplication.primaryScreen()
            if screen:
                screen_geometry = screen.geometry()
                self.setGeometry(screen_geometry)
        super().showEvent(event)

    def paintEvent(self, event):
        # Draw blurred black background (simulate with semi-transparent black)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 180))  # 180 = ~70% opacity
        super().paintEvent(event)

    def update_time(self):
        now = QTime.currentTime().toString("HH:mm")
        self.time_label.setText(now)

    def accept(self):
        self.sound.stop()
        super().accept()

    def handle_snooze(self):
        self.sound.stop()
        self.accept()