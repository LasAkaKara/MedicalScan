from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap, QIcon, QPainter, QPen, QColor, QRegion, QPainterPath
from PySide6.QtCore import Qt, QSize, QRect
from themes import PRIMARY_COLOR

class ScanZoneOverlay(QWidget):
    def __init__(self, parent=None, vertical_offset=0):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.corner_radius = 40
        self.rect_width = 320
        self.rect_height = 480
        self.vertical_offset = 20

    def setVerticalOffset(self, offset):
        self.vertical_offset = offset
        self.update()
        self.resizeEvent(None)

    def get_scan_zone_rect(self):
        """Get the actual scan zone rectangle coordinates"""
        w, h = self.rect_width, self.rect_height
        scale = 0.989
        w_scaled = int(w * scale)
        h_scaled = int(h * scale)
        x_scaled = (self.width() - w_scaled) // 2
        y_scaled = (self.height() - h_scaled) // 2 - self.vertical_offset
        return QRect(x_scaled, y_scaled, w_scaled, h_scaled)

    def resizeEvent(self, event):
        w, h = self.rect_width, self.rect_height
        outer = QRegion(self.rect())

        scale = 0.989
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

        # Draw semi-transparent overlay
        overlay_color = QColor(0, 0, 0, 120)
        painter.setBrush(overlay_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # Draw scan zone guidelines
        w, h = self.rect_width, self.rect_height
        x = (self.width() - w) // 2
        y = (self.height() - h) // 2 - self.vertical_offset
        r = self.corner_radius

        # Draw corner guides
        pen = QPen(QColor(255, 255, 255), 4)
        painter.setPen(pen)
        arc_len = 16*90
        
        corner_length = 30
        
        # Top-left corner
        painter.drawLine(x, y + r, x, y + r - corner_length)
        painter.drawLine(x + r - corner_length, y, x + r, y)
        painter.drawArc(x, y, 2*r, 2*r, 16*90, arc_len)
        
        # Top-right corner
        painter.drawLine(x + w, y + r - corner_length, x + w, y + r)
        painter.drawLine(x + w - r, y, x + w - r + corner_length, y)
        painter.drawArc(x+w-2*r, y, 2*r, 2*r, 0, arc_len)
        
        # Bottom-left corner
        painter.drawLine(x, y + h - r, x, y + h - r + corner_length)
        painter.drawLine(x + r - corner_length, y + h, x + r, y + h)
        painter.drawArc(x, y+h-2*r, 2*r, 2*r, 16*180, arc_len)
        
        # Bottom-right corner
        painter.drawLine(x + w, y + h - r + corner_length, x + w, y + h - r)
        painter.drawLine(x + w - r + corner_length, y + h, x + w - r, y + h)
        painter.drawArc(x+w-2*r, y+h-2*r, 2*r, 2*r, 16*270, arc_len)

        # Add instruction text
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawText(x, y - 40, w, 30, Qt.AlignCenter, "Đặt đơn thuốc vào khung này, đảm bảo môi trường ánh sáng đầy đủ")

class IPhoneCaptureButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)
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

        # Quality indicator (top right)
        self.quality_indicator = QLabel(self)
        self.quality_indicator.setText("📷 Chất lượng: Tốt")
        self.quality_indicator.setStyleSheet("""
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 8px 12px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: bold;
        """)
        self.quality_indicator.move(self.width() - 150, 16)
        self.quality_indicator.raise_()

        # Bottom background for capture/upload buttons
        self.bottom_bg = QWidget(self)
        self.bottom_bg.setGeometry(0, self.height() - 100, self.width(), 100)
        self.bottom_bg.setStyleSheet("background: rgba(0,0,0,0.7); border-top-left-radius: 24px; border-top-right-radius: 24px;")

        # Layout for bottom_bg
        self.bottom_bg_layout = QHBoxLayout(self.bottom_bg)
        self.bottom_bg_layout.setContentsMargins(16, 0, 16, 0)
        self.bottom_bg_layout.setSpacing(24)

        # Capture and upload buttons
        self.capture_btn = QPushButton(self.bottom_bg)
        self.capture_btn.setFixedSize(80, 80)
        self.capture_btn.setStyleSheet("""
            QPushButton {
                background: white;
                border: 4px solid #ddd;
                border-radius: 40px;
            }
            QPushButton:pressed {
                background: #f0f0f0;
            }
        """)
        
        self.upload_btn = QPushButton(self.bottom_bg)
        self.upload_btn.setIcon(QIcon("assets/copy-image.png"))
        self.upload_btn.setIconSize(QSize(36, 36))
        self.upload_btn.setFixedSize(56, 56)
        self.upload_btn.setStyleSheet("border-radius: 28px; background: #7FACB7;")

        # Add buttons to layout
        self.bottom_bg_layout.addStretch()
        self.bottom_bg_layout.addStretch()
        self.bottom_bg_layout.addWidget(self.capture_btn, alignment=Qt.AlignVCenter)
        self.bottom_bg_layout.addStretch()
        self.bottom_bg_layout.addWidget(self.upload_btn, alignment=Qt.AlignVCenter | Qt.AlignRight)

        # Bottom controls
        self.bottom_controls = QWidget(self)
        self.bottom_controls.setGeometry(0, self.height() - 100, self.width(), 120)
        self.bottom_layout = QHBoxLayout(self.bottom_controls)
        self.bottom_layout.setContentsMargins(24, 0, 24, 0)
        self.bottom_layout.setSpacing(24)
        self.bottom_controls.setStyleSheet("background: rgba(0,0,0,0.7); border-top-left-radius: 24px; border-top-right-radius: 24px;")
        self.bottom_controls.hide()

        # Control buttons
        self.retake_btn = QPushButton(self)
        self.retake_btn.setIcon(QIcon("assets/arrow-circle-right.png"))
        self.retake_btn.setIconSize(QSize(40, 40))
        self.retake_btn.setFixedSize(56, 56)
        self.retake_btn.setStyleSheet("border-radius: 28px; background: transparent;")
        self.retake_btn.hide()

        self.confirm_btn = QPushButton(self)
        self.confirm_btn.setIcon(QIcon("assets/check.png"))
        self.confirm_btn.setIconSize(QSize(48, 48))
        self.confirm_btn.setFixedSize(72, 72)
        self.confirm_btn.setStyleSheet(f"border-radius: 28px; background: {PRIMARY_COLOR}; color: white;")
        self.confirm_btn.hide()

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
        self.quality_indicator.move(self.width() - 150, 16)
        super().resizeEvent(event)

    def show_capture_controls(self):
        self.capture_btn.show()
        self.upload_btn.show()
        self.capture_btn.raise_()
        self.upload_btn.raise_()
        self.bottom_controls.hide()

    def show_bottom_controls(self):
        self.capture_btn.hide()
        self.upload_btn.hide()
        self.bottom_controls.show()
        self.bottom_controls.raise_()

    def update_quality_indicator(self, quality_score, quality_text):
        """Update the quality indicator based on image analysis"""
        if quality_score >= 0.8:
            color = "#22c55e"  # Green
            icon = "✅"
        elif quality_score >= 0.6:
            color = "#f59e0b"  # Orange
            icon = "⚠️"
        else:
            color = "#ef4444"  # Red
            icon = "❌"
        
        self.quality_indicator.setText(f"{icon} {quality_text}")
        self.quality_indicator.setStyleSheet(f"""
            background: {color};
            color: white;
            padding: 8px 12px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: bold;
        """)