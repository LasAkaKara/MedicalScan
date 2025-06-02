from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon, QPainter, QPen, QColor, QRegion, QPainterPath
from PySide6.QtCore import Qt, QSize, QRect
from themes import PRIMARY_COLOR

class ScanZoneOverlay(QWidget):
    def __init__(self, parent=None, vertical_offset=0):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.corner_radius = 40
        self.rect_width = 300
        self.rect_height = 500
        self.vertical_offset = 20  # Positive value pushes up

    def setVerticalOffset(self, offset):
        self.vertical_offset = offset
        self.update()
        self.resizeEvent(None)

    def resizeEvent(self, event):
        w, h = self.rect_width, self.rect_height
        outer = QRegion(self.rect())

        # Create a rounded rectangle path for the scan zone
        scale = 0.989  # Scale down by 2%
        w_scaled = int(w * scale)
        h_scaled = int(h * scale)
        x_scaled = (self.width() - w_scaled) // 2
        y_scaled = (self.height() - h_scaled) // 2 - self.vertical_offset

        path = QPainterPath()
        path.addRoundedRect(x_scaled, y_scaled, w_scaled, h_scaled, self.corner_radius, self.corner_radius)
        inner = QRegion(path.toFillPolygon().toPolygon())

        mask = outer.subtracted(inner)
        self.setMask(mask)
        if event:
            super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Draw semi-transparent overlay (the mask ensures the scan zone is a hole)
        overlay_color = QColor(0, 0, 0, 100)
        painter.setBrush(overlay_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # 2. Draw white rounded corners for the scan zone
        w, h = self.rect_width, self.rect_height
        x = (self.width() - w) // 2
        y = (self.height() - h) // 2 - self.vertical_offset
        r = self.corner_radius

        pen = QPen(QColor(255, 255, 255), 5)
        painter.setPen(pen)
        arc_len = 16*90
        # Top-left
        painter.drawArc(x, y, 2*r, 2*r, 16*90, arc_len)
        # Top-right
        painter.drawArc(x+w-2*r, y, 2*r, 2*r, 0, arc_len)
        # Bottom-left
        painter.drawArc(x, y+h-2*r, 2*r, 2*r, 16*180, arc_len)
        # Bottom-right
        painter.drawArc(x+w-2*r, y+h-2*r, 2*r, 2*r, 16*270, arc_len)



class IPhoneCaptureButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)  # iPhone-like size
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Outer ring
        ring_color = QColor(220, 220, 220)
        pen = QPen(ring_color, 4)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(2, 2, self.width()-4, self.height()-4)

        # Inner circle
        inner_radius = self.width() * 0.76
        offset = (self.width() - inner_radius) / 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(int(offset), int(offset), int(inner_radius), int(inner_radius))

class ScanScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quét tài liệu")
        self.setMinimumSize(400, 700)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        # Camera preview label (fills the widget)
        self.camera_label = QLabel(self)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setGeometry(0, 0, self.width(), self.height())
        self.camera_label.setStyleSheet("background: transparent;")

        self.camera_label.setPixmap(QPixmap("assets/avatar_placeholder.png").scaled(
            self.camera_label.width(),
            self.camera_label.height(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        ))

        # Overlay for scan zone
        self.scan_zone_overlay = ScanZoneOverlay(self)
        self.scan_zone_overlay.setGeometry(0, 0, self.width(), self.height())
        self.scan_zone_overlay.raise_()

        # Back button (top left)
        self.back_btn = QPushButton(self)
        self.back_btn.setIcon(QIcon("assets/close.png"))
        self.back_btn.setIconSize(QSize(32, 32))
        self.back_btn.setFixedSize(48, 48)
        self.back_btn.move(16, 16)
        self.back_btn.raise_()

        # --- Bottom background for capture/upload buttons ---
        self.bottom_bg = QWidget(self)
        self.bottom_bg.setGeometry(0, self.height() - 100, self.width(), 100)
        self.bottom_bg.setStyleSheet("background: rgba(0,0,0,0.7); border-top-left-radius: 24px; border-top-right-radius: 24px;")

        # Layout for bottom_bg
        self.bottom_bg_layout = QHBoxLayout(self.bottom_bg)
        self.bottom_bg_layout.setContentsMargins(16, 0, 16, 0)  # Reduce margins
        self.bottom_bg_layout.setSpacing(24)

        # Capture and upload buttons
        self.capture_btn = IPhoneCaptureButton(self.bottom_bg)
        self.upload_btn = QPushButton(self.bottom_bg)
        self.upload_btn.setIcon(QIcon("assets/copy-image.png"))
        self.upload_btn.setIconSize(QSize(36, 36))
        self.upload_btn.setFixedSize(56, 56)
        self.upload_btn.setStyleSheet("border-radius: 28px; background: #7FACB7;")

        # Add buttons to layout: center capture, right upload
        self.bottom_bg_layout.addStretch()  # Center capture button
        self.bottom_bg_layout.addStretch()
        self.bottom_bg_layout.addWidget(self.capture_btn, alignment=Qt.AlignVCenter)
        self.bottom_bg_layout.addStretch()
        self.bottom_bg_layout.addWidget(self.upload_btn, alignment=Qt.AlignVCenter | Qt.AlignRight)

        # --- Bottom controls ---
        self.bottom_controls = QWidget(self)
        self.bottom_controls.setGeometry(0, self.height() - 100, self.width(), 120)
        self.bottom_layout = QHBoxLayout(self.bottom_controls)
        self.bottom_layout.setContentsMargins(24, 0, 24, 0)
        self.bottom_layout.setSpacing(24)
        self.bottom_controls.setStyleSheet("background: rgba(0,0,0,0.7); border-top-left-radius: 24px; border-top-right-radius: 24px;")
        self.bottom_controls.hide()

        # Back button (hidden by default)
        self.retake_btn = QPushButton(self)
        self.retake_btn.setIcon(QIcon("assets/arrow-circle-right.png"))
        self.retake_btn.setIconSize(QSize(40, 40))
        self.retake_btn.setFixedSize(56, 56)
        self.retake_btn.setStyleSheet("border-radius: 28px; background: transparent;")
        self.retake_btn.hide()

        # Confirm button (hidden by default)
        self.confirm_btn = QPushButton(self)
        self.confirm_btn.setIcon(QIcon("assets/check.png"))
        self.confirm_btn.setIconSize(QSize(48, 48))
        self.confirm_btn.setFixedSize(72, 72)
        self.confirm_btn.setStyleSheet(f"border-radius: 28px; background: {PRIMARY_COLOR}; color: white;")
        self.confirm_btn.hide()

        # Save button (hidden by default)
        self.save_btn = QPushButton(self)
        self.save_btn.setIcon(QIcon("assets/save.png"))
        self.save_btn.setIconSize(QSize(40, 40))
        self.save_btn.setFixedSize(56, 56)
        self.save_btn.setStyleSheet("border-radius: 28px; background: transparent; color: white;")
        self.save_btn.hide()

        # Add to layout
        self.bottom_layout.addWidget(self.retake_btn)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.confirm_btn)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.save_btn)

        self.capture_btn.raise_()
        self.upload_btn.raise_()

    def resizeEvent(self, event):
        self.camera_label.setGeometry(0, 0, self.width(), self.height())
        self.scan_zone_overlay.setGeometry(0, 0, self.width(), self.height())
        self.bottom_bg.setGeometry(0, self.height() - 100, self.width(), 100)
        self.bottom_controls.setGeometry(0, self.height() - 100, self.width(), 100)
        super().resizeEvent(event)

    # Utility methods for logic class:
    def show_capture_controls(self):
        self.capture_btn.show()
        self.upload_btn.show()
        self.capture_btn.raise_()
        self.upload_btn.raise_()
        self.bottom_controls.hide()
        self.reset_camera_label_drag()

    def show_bottom_controls(self):
        self.capture_btn.hide()
        self.upload_btn.hide()
        self.bottom_controls.show()
        self.bottom_controls.raise_()