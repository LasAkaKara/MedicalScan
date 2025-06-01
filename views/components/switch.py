from PySide6.QtWidgets import QCheckBox, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QRectF, QSize

class QSwitch(QCheckBox):
    """A simple switch widget for PySide6."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTristate(False)
        self.setMinimumSize(40, 22)
        self.setMaximumHeight(22)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("QCheckBox { background: transparent; }")
        self.setFocusPolicy(Qt.StrongFocus)

    def sizeHint(self):
        return QSize(40, 22)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Draw background
        if self.isChecked():
            bg_color = QColor("#4CAF50")
        else:
            bg_color = QColor("#ccc")
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        rect = QRectF(0, 0, 40, 22)
        painter.drawRoundedRect(rect, 11, 11)
        # Draw handle
        handle_color = QColor("#fff")
        painter.setBrush(QBrush(handle_color))
        if self.isChecked():
            handle_rect = QRectF(20, 2, 18, 18)
        else:
            handle_rect = QRectF(2, 2, 18, 18)
        painter.drawEllipse(handle_rect)
        # Draw focus border if focused
        if self.hasFocus():
            pen = QPen(QColor("#2196F3"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 11, 11)
        painter.end()
    
    def hitButton(self, pos):
        # Always return True so any click inside the widget toggles the switch
        return True