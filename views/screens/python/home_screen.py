from PySide6.QtCore import Signal
from views.screens.pyside.home_screen_ui import HomeScreenUI
from PySide6.QtWidgets import QMessageBox

class HomeScreen(HomeScreenUI):
    go_to_scan = Signal()
    go_to_prescription = Signal()
    go_to_calendar = Signal()
    go_to_settings = Signal()
    go_to_login = Signal()
    go_to_profile = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logout_btn.clicked.connect(self.handle_logout)
        self.avatar_label.mousePressEvent = lambda event: self.go_to_profile.emit()

        # Connect feature boxes to navigation
        if len(self.feature_boxes) >= 4:
            self.feature_boxes[0].clicked.connect(self.go_to_scan.emit)
            self.feature_boxes[1].clicked.connect(self.go_to_prescription.emit)
            self.feature_boxes[2].clicked.connect(self.go_to_calendar.emit)
            self.feature_boxes[3].clicked.connect(self.go_to_settings.emit)

    def handle_logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.go_to_login.emit()