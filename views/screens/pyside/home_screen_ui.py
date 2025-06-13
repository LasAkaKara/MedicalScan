from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QGridLayout
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, Signal
from themes import PRIMARY_COLOR, FONT_FAMILY, FONT_SIZE_SM ,FONT_SIZE_MD, FONT_SIZE_LG, HINT_COLOR, TEXT_COLOR

class FeatureBox(QWidget):
    clicked = Signal()

    def __init__(self, image_path, title, bg_color="#fff", parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 250)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(6)
        self.setStyleSheet(f"""
            background: {bg_color};
            border-radius: 20px;
            border: 1px solid #e0e0e0;
            padding: 16px;
        """)

        # Feature image
        img_label = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            img_label.setPixmap(pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(img_label)
        # Feature title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; font-weight: 600; color: #344054; background: transparent; font-family: {FONT_FAMILY}; padding: 0px; border: none;")
        layout.addWidget(title_label)

    def mousePressEvent(self, event):
        self.clicked.emit()

class HomeScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MediScan - Home")
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # --- Top user info container ---
        user_container = QHBoxLayout()
        user_container.setAlignment(Qt.AlignVCenter)
        user_container.setSpacing(12)

        # Avatar
        self.avatar_label = QLabel()
        avatar_pixmap = QPixmap("assets/circle-user.png")
        if not avatar_pixmap.isNull():
            self.avatar_label.setPixmap(avatar_pixmap.scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.avatar_label.setFixedSize(56, 56)
        self.avatar_label.setStyleSheet("border-radius: 28px; background: #e3eaf6;")
        user_container.addWidget(self.avatar_label)

        # Greeting and subtitle
        greet_layout = QVBoxLayout()
        greet_layout.setSpacing(2)
        self.greet_label = QLabel("Hi, user!")  # <-- Make it an attribute!
        self.greet_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {TEXT_COLOR}")
        greet_layout.addWidget(self.greet_label)
        subtitle_label = QLabel("Hãy nhớ uống thuốc nhé")
        subtitle_label.setStyleSheet(f"font-size: 13px; color: #406D96; color: {HINT_COLOR}")
        greet_layout.addWidget(subtitle_label)
        user_container.addLayout(greet_layout)

        user_container.addStretch()

        # Notification bell
        self.bell_btn = QPushButton()
        self.bell_btn.setIcon(QIcon("assets/bell.png"))
        self.bell_btn.setIconSize(QSize(28, 28))
        self.bell_btn.setFixedSize(36, 36)
        self.bell_btn.setStyleSheet("background: #F1F9FF; border-radius: 32px; padding: 4px")
        user_container.addWidget(self.bell_btn)

        main_layout.addLayout(user_container)

        # --- Features grid ---
        features_grid = QGridLayout()
        features_grid.setSpacing(0)

        # Example feature boxes with custom background colors
        feature_data = [
            ("assets/camera.png", "Quét đơn thuốc", PRIMARY_COLOR),
            ("assets/medical-prescription.png", "Xem đơn thuốc", "#FAF1DE"), 
            ("assets/calendar.png", "Lịch uống thuốc", "#C0E7E7"),       # Light green
            ("assets/setting.png", "Cài đặt", "#666666")  # Light orange
        ]
        self.feature_boxes = []
        for i, (img, title, bg_color) in enumerate(feature_data):
            box = FeatureBox(img, title, bg_color)
            self.feature_boxes.append(box)
            row, col = divmod(i, 2)
            features_grid.addWidget(box, row, col)

        main_layout.addLayout(features_grid)

        # Spacer at the bottom
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Logout Button (optional, can be moved elsewhere)
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setStyleSheet("color: #F44336; background: transparent; font-size: 14px;")
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(self.logout_btn, alignment=Qt.AlignCenter)