from PySide6.QtCore import Signal
from views.screens.pyside.home_screen import HomeScreenUI
from PySide6.QtWidgets import QMessageBox

class HomeScreen(HomeScreenUI):
    go_to_scan = Signal()
    go_to_login = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scan_btn.clicked.connect(self.handle_scan)
        self.logout_btn.clicked.connect(self.handle_logout)

    def handle_scan(self):
        # You can add logic here before switching to scan screen
        self.go_to_scan.emit()

    def handle_logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.go_to_login.emit()