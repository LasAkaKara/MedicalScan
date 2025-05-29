from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtGui import QPixmap, QIcon, QPainter, QPen
from PySide6.QtCore import Qt, QSize, QRect, QPoint

class CropOverlay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setMouseTracking(True)
        self.crop_rect = QRect(60, 60, 200, 200)
        self.dragging = False
        self.drag_offset = QPoint()
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.green, 3)
        painter.setPen(pen)
        painter.drawRect(self.crop_rect)

    def mousePressEvent(self, event):
        if self.crop_rect.contains(event.pos()):
            self.dragging = True
            self.drag_offset = event.pos() - self.crop_rect.topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging:
            top_left = event.pos() - self.drag_offset
            # Keep the rect within the widget
            top_left.setX(max(0, min(top_left.x(), self.width() - self.crop_rect.width())))
            top_left.setY(max(0, min(top_left.y(), self.height() - self.crop_rect.height())))
            self.crop_rect.moveTopLeft(top_left)
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def get_crop_rect(self):
        return self.crop_rect

class ScanScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quét tài liệu")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setSpacing(24)
        self.main_layout.setContentsMargins(24, 24, 24, 24)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignVCenter)
        header_layout.setSpacing(12)

        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon("assets/arrow-left.png"))
        self.back_btn.setIconSize(QSize(32, 32))
        self.back_btn.setFixedSize(40, 40)
        self.back_btn.setStyleSheet("border: none; background: transparent;")
        header_layout.addWidget(self.back_btn)

        title_layout = QVBoxLayout()
        title_label = QLabel("Quét tài liệu")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #002D40;")
        subtitle_label = QLabel("Quét đơn thuốc của bạn tại đây")
        subtitle_label.setStyleSheet("font-size: 16px; color: #667085;")
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QIcon("assets/cog.png"))
        self.settings_btn.setIconSize(QSize(32, 32))
        self.settings_btn.setFixedSize(40, 40)
        self.settings_btn.setStyleSheet("border: none; background: transparent;")
        header_layout.addWidget(self.settings_btn)

        self.main_layout.addLayout(header_layout)

        # Image area
        self.image_frame = QFrame()
        self.image_frame.setStyleSheet("background: #000;")
        self.image_frame.setMinimumSize(320, 320)
        self.image_layout = QVBoxLayout(self.image_frame)
        self.image_layout.setContentsMargins(0, 0, 0, 0)
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.image_layout.addWidget(self.camera_label)
        self.crop_overlay = CropOverlay(self.camera_label)
        self.crop_overlay.setGeometry(0, 0, 320, 320)
        self.crop_overlay.hide()
        self.main_layout.addWidget(self.image_frame)

        # Controls area (dynamic)
        self.controls_area = QHBoxLayout()
        self.controls_area.setAlignment(Qt.AlignCenter)
        self.controls_area.setSpacing(24)
        self.main_layout.addLayout(self.controls_area)

        # Initial controls
        self.capture_btn = QPushButton()
        self.capture_btn.setIcon(QIcon("assets/camera.png"))
        self.capture_btn.setIconSize(QSize(48, 48))
        self.capture_btn.setFixedSize(64, 64)
        self.capture_btn.setStyleSheet("border-radius: 32px; background: #406D96;")

        self.upload_btn = QPushButton()
        self.upload_btn.setIcon(QIcon("assets/upload.png"))
        self.upload_btn.setIconSize(QSize(48, 48))
        self.upload_btn.setFixedSize(64, 64)
        self.upload_btn.setStyleSheet("border-radius: 32px; background: #406D96;")

        self.crop_back_btn = QPushButton("Chụp lại")
        self.auto_detect_btn = QPushButton("Tự động")
        self.rotate_btn = QPushButton("Xoay")
        self.confirm_btn = QPushButton("Xác nhận")
        for btn in [self.crop_back_btn, self.auto_detect_btn, self.rotate_btn, self.confirm_btn]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("font-size: 16px; border-radius: 8px; background: #406D96; color: white;")

        # Add initial controls
        self.controls_area.addWidget(self.capture_btn)
        self.controls_area.addWidget(self.upload_btn)

    def show_crop_controls(self):
        # Remove all widgets from controls_area
        while self.controls_area.count():
            item = self.controls_area.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        # Add crop controls (do NOT recreate them)
        for btn in [self.crop_back_btn, self.auto_detect_btn, self.rotate_btn, self.confirm_btn]:
            self.controls_area.addWidget(btn)
        self.crop_overlay.show()

    def show_capture_controls(self):
        # Remove all widgets from controls_area
        while self.controls_area.count():
            item = self.controls_area.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        self.controls_area.addWidget(self.capture_btn)
        self.controls_area.addWidget(self.upload_btn)
        self.crop_overlay.hide()