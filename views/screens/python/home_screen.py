from PySide6.QtCore import Signal
from views.screens.pyside.home_screen_ui import HomeScreenUI
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, Qt
from urllib.request import urlopen
from services.database_service import DatabaseService
from views.components.loading_overlay import LoadingOverlay

class HomeScreen(HomeScreenUI):
    go_to_scan = Signal()
    go_to_prescription = Signal()
    go_to_calendar = Signal()
    go_to_settings = Signal()
    go_to_login = Signal()
    go_to_profile = Signal()
    go_to_notification = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loading_overlay = LoadingOverlay(self)
        self.logout_btn.clicked.connect(self.handle_logout)
        self.bell_btn.clicked.connect(self.go_to_notification.emit)
        self.avatar_label.mousePressEvent = lambda event: self.go_to_profile.emit()
        self.db = DatabaseService()

        # Connect feature boxes to navigation
        if len(self.feature_boxes) >= 4:
            self.feature_boxes[0].clicked.connect(self.go_to_scan.emit)
            self.feature_boxes[1].clicked.connect(self.go_to_prescription.emit)
            self.feature_boxes[2].clicked.connect(self.go_to_calendar.emit)
            self.feature_boxes[3].clicked.connect(self.go_to_settings.emit)

    def set_user(self, email):
        """Load and display the current user's info on the home screen."""
        user = self.db.get_user_by_email(email)
        if user:
            if hasattr(self, "greet_label"):
                name = user.get('full_name') or "User"
                self.greet_label.setText(f"Hi, {name}!")
        # Set avatar
        avatar_url = user.get("avatar_url")
        pixmap = None
        if avatar_url:
            try:
                data = urlopen(avatar_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
            except Exception:
                pixmap = QPixmap("assets/circle-user.png")
        else:
            pixmap = QPixmap("assets/circle-user.png")
        if not pixmap.isNull():
            self.avatar_label.setPixmap(self.get_rounded_pixmap(pixmap, 56))

    def handle_logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.go_to_login.emit()

    def get_rounded_pixmap(self, pixmap, size=56):
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return rounded