# #:import utils kivy.utils
# #:import dp kivy.metrics.dp

# <SettingsScreen>:
#     BoxLayout:
#         orientation: 'vertical'
        
#         # Header with back button
#         Header:
        
#         # Settings content in a scroll view
#         ScrollView:
#             BoxLayout:
#                 orientation: 'vertical'
#                 size_hint_y: None
#                 height: self.minimum_height
#                 padding: dp(16)
#                 spacing: dp(12)
#                 # Camera settings
#                 MDCard:
#                     orientation: "vertical"
#                     padding: dp(16)
#                     size_hint_x: None
#                     spacing: dp(12)
#                     width: dp(360)
#                     size_hint_y: None
#                     height: self.minimum_height
#                     md_bg_color: 1, 1, 1, 1
#                     radius: [8]
#                     pos_hint: {"center_x": 0.5}
                    
#                     MDLabel:
#                         text: "Camera Settings"
#                         halign: "left"
#                         theme_text_color: "Primary"
#                         font_style: "H6"
#                         size_hint_y: None
#                         height: dp(48)
                    
#                     MDSeparator:
#                         height: "1dp"
                    
#                     # Camera flip
#                     BoxLayout:
#                         orientation: "horizontal"
#                         height: dp(60)
#                         size_hint_y: None
#                         size_hint_x: 1
#                         spacing: dp(8)
#                         padding: [0, 0, 22, 0]
                        
#                         MDLabel:
#                             text: "Flip Camera Horizontally"
#                             theme_text_color: "Primary"
#                             size_hint_x: 1
                        
#                         MDSwitch:
#                             size_hint_x: None
#                             width: dp(48)
#                             active: root.camera_flip_horizontal
#                             on_active: root.toggle_camera_flip_horizontal()
                        
                    
#                     BoxLayout:
#                         orientation: "horizontal"
#                         height: dp(60)
#                         size_hint_y: None
#                         spacing: dp(8)
#                         padding: [0, 0, 22, 0]
                        
#                         MDLabel:
#                             text: "Flip Camera Vertically"
#                             theme_text_color: "Primary"
#                             size_hint_x: 1
                        
#                         MDSwitch:
#                             size_hint_x: None
#                             width: dp(48)
#                             active: root.camera_flip_vertical
#                             on_active: root.toggle_camera_flip_vertical()
                    
#                     # Camera resolution
#                     BoxLayout:
#                         orientation: "horizontal"
#                         height: dp(60)
#                         size_hint_y: None
#                         spacing: dp(8)
                        
#                         MDLabel:
#                             text: "Camera Resolution"
#                             theme_text_color: "Primary"
#                             size_hint_x: 1
                        
#                         Spinner:
#                             id: camera_resolution
#                             text: root.camera_resolution
#                             values: ["640x480", "800x600", "1280x720", "1920x1080"]
#                             on_text: root.set_camera_resolution(self.text)
                    
#                     # Camera quality
#                     BoxLayout:
#                         orientation: "horizontal"
#                         height: dp(60)
#                         size_hint_y: None
#                         spacing: dp(8)
                        
#                         MDLabel:
#                             text: "Image Quality: " + str(int(quality_slider.value)) + "%"
#                             theme_text_color: "Primary"
#                             size_hint_x: 1
                        
#                         MDSlider:
#                             id: quality_slider
#                             min: 10
#                             max: 100
#                             value: root.camera_quality
#                             on_value: root.set_camera_quality(self.value)
                
#                 # App settings
#                 MDCard:
#                     orientation: "vertical"
#                     padding: dp(16)
#                     size_hint_x: None
#                     spacing: dp(12)
#                     width: dp(360)
#                     size_hint_y: None
#                     height: self.minimum_height
#                     md_bg_color: 1, 1, 1, 1
#                     radius: [8]
#                     pos_hint: {"center_x": 0.5}
                    
#                     MDLabel:
#                         text: "App Settings"
#                         halign: "left"
#                         theme_text_color: "Primary"
#                         font_style: "H6"
#                         size_hint_y: None
#                         height: dp(48)
                    
#                     MDSeparator:
#                         height: "1dp"
                    
#                     # Auto detect documents
#                     BoxLayout:
#                         orientation: "horizontal"
#                         height: dp(60)
#                         size_hint_y: None
#                         spacing: dp(8)
#                         padding: [0, 0, 22, 0]
                        
#                         MDLabel:
#                             text: "Auto-detect Documents"
#                             theme_text_color: "Primary"
#                             size_hint_x: 1
                        
#                         MDSwitch:
#                             size_hint_x: None
#                             width: dp(48)
#                             active: root.auto_detect_documents
#                             on_active: root.toggle_auto_detect_documents()
                    
#                     # Save original images
#                     BoxLayout:
#                         orientation: "horizontal"
#                         height: dp(60)
#                         size_hint_y: None
#                         spacing: dp(8)
#                         padding: [0, 0, 22, 0]
                        
#                         MDLabel:
#                             text: "Save Original Images"
#                             theme_text_color: "Primary"
#                             size_hint_x: 1
                        
#                         MDSwitch:
#                             size_hint_x: None
#                             width: dp(48)
#                             active: root.save_original_images
#                             on_active: root.toggle_save_original_images()
                
#                 # Theme settings
#                 MDCard:
#                     orientation: "vertical"
#                     padding: dp(16)
#                     size_hint_x: None
#                     spacing: dp(12)
#                     width: dp(360)
#                     size_hint_y: None
#                     height: self.minimum_height
#                     md_bg_color: 1, 1, 1, 1
#                     radius: [8]
#                     pos_hint: {"center_x": 0.5}
                    
#                     MDLabel:
#                         text: "Theme Settings"
#                         halign: "left"
#                         theme_text_color: "Primary"
#                         font_style: "H6"
#                         size_hint_y: None
#                         height: dp(48)
                    
#                     MDSeparator:
#                         height: "1dp"
                    
#                     # Dark mode
#                     BoxLayout:
#                         orientation: "horizontal"
#                         height: dp(60)
#                         size_hint_y: None
#                         spacing: dp(8)
#                         padding: [0, 0, 22, 0]
                        
#                         MDLabel:
#                             text: "Dark Mode"
#                             theme_text_color: "Primary"
#                             size_hint_x: 1
                        
#                         MDSwitch:
#                             size_hint_x: None
#                             width: dp(48)
#                             on_active: app.root.toggle_theme()
                
#                 # Save button
#                 BoxLayout:
#                     orientation: "horizontal"
#                     size_hint_y: None
#                     height: dp(60)
#                     padding: dp(16)
                    
#                     Widget:
#                         size_hint_x: 0.7
                    
#                     MDRaisedButton:
#                         text: "Save Settings"
#                         on_release: root.save_settings() 

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QSlider, QFrame, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from views.components.switch import QSwitch
from themes import PRIMARY_COLOR, FONT_FAMILY, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG, HINT_COLOR, TEXT_COLOR

class SettingsScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Header
        header = QLabel("Cài đặt")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #002D40;")
        main_layout.addWidget(header)

        # --- Camera Settings Card ---
        camera_card = QFrame()
        camera_card.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
                font-family: Roboto, sans-serif;
            }
        """)
        card_shadow = QGraphicsDropShadowEffect(self)
        card_shadow.setBlurRadius(12)
        card_shadow.setOffset(0, 4)
        card_shadow.setColor(Qt.gray)
        camera_card.setGraphicsEffect(card_shadow)
        camera_layout = QVBoxLayout(camera_card)
        camera_layout.setSpacing(14)
        camera_layout.setContentsMargins(18, 18, 18, 18)

        camera_title = QLabel("Cài đặt Camera")
        camera_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #406D96; border: none;")
        camera_layout.addWidget(camera_title)

        # Flip horizontal
        flip_h_row = QHBoxLayout()
        flip_h_label = QLabel("Lật ngang camera")
        flip_h_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; border: none;")
        self.flip_h_switch = QSwitch()
        flip_h_row.addWidget(flip_h_label)
        flip_h_row.addStretch()
        flip_h_row.addWidget(self.flip_h_switch)
        camera_layout.addLayout(flip_h_row)

        # Flip vertical
        flip_v_row = QHBoxLayout()
        flip_v_label = QLabel("Lật dọc camera")
        flip_v_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; border: none;")
        self.flip_v_switch = QSwitch()
        flip_v_row.addWidget(flip_v_label)
        flip_v_row.addStretch()
        flip_v_row.addWidget(self.flip_v_switch)
        camera_layout.addLayout(flip_v_row)

        # Camera resolution
        res_row = QHBoxLayout()
        res_label = QLabel("Độ phân giải camera:")
        res_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; border: none;")
        self.res_combo = QComboBox()
        self.res_combo.setStyleSheet("""
            QComboBox {
            border: 1px solid #406D96;
            padding: 0px 24px 0px 10px;
            font-size: 15px;
            color: #002D40;
            background: #f7fafc;
            min-width: 120px;
            }
            QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 24px;
            background: #e3eaf2;
            }
            QComboBox::down-arrow {
            image: url(assets/down-arrow.png);
            width: 16px;
            height: 16px;
            }
            QComboBox QAbstractItemView {
            border: 1px solid #406D96;
            border-radius: 0px;
            background: #fff;
            font-size: 15px;
            }
        """)
        self.res_combo.addItems(["640x480", "800x600", "1280x720", "1920x1080"])
        res_row.addWidget(res_label)
        res_row.addStretch()
        res_row.addWidget(self.res_combo)
        camera_layout.addLayout(res_row)

        # Camera quality
        qual_row = QHBoxLayout()
        qual_label = QLabel("Chất lượng ảnh:")
        qual_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; border: none;")
        qual_row.addWidget(qual_label)
        qual_row.addStretch()
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(50)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(80)
        self.quality_slider.setFixedWidth(120)
        self.quality_slider.valueChanged.connect(self._update_quality_label)
        qual_row.addWidget(self.quality_slider)
        self.quality_value_label = QLabel(f"{self.quality_slider.value()}%")
        self.quality_value_label.setStyleSheet("font-size: 14px; min-width: 36px; color: #406D96; border: none;")
        qual_row.addWidget(self.quality_value_label)
        camera_layout.addLayout(qual_row)

        main_layout.addWidget(camera_card)

        # --- App Settings Card ---
        app_card = QFrame()
        app_card.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
            }
        """)
        app_shadow = QGraphicsDropShadowEffect(self)
        app_shadow.setBlurRadius(12)
        app_shadow.setOffset(0, 4)
        app_shadow.setColor(Qt.gray)
        app_card.setGraphicsEffect(app_shadow)
        app_layout = QVBoxLayout(app_card)
        app_layout.setSpacing(14)
        app_layout.setContentsMargins(18, 18, 18, 18)

        app_title = QLabel("Cài đặt Ứng dụng")
        app_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #406D96; border: none;")
        app_layout.addWidget(app_title)

        # Auto-detect documents
        auto_detect_row = QHBoxLayout()
        auto_detect_label = QLabel("Tự động phát hiện tài liệu")
        auto_detect_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; border: none;")
        self.auto_detect_switch = QSwitch()
        auto_detect_row.addWidget(auto_detect_label)
        auto_detect_row.addStretch()
        auto_detect_row.addWidget(self.auto_detect_switch)
        app_layout.addLayout(auto_detect_row)

        # Save original images
        save_original_row = QHBoxLayout()
        save_original_label = QLabel("Lưu ảnh gốc")
        save_original_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; border: none;")
        self.save_original_switch = QSwitch()
        save_original_row.addWidget(save_original_label)
        save_original_row.addStretch()
        save_original_row.addWidget(self.save_original_switch)
        app_layout.addLayout(save_original_row)

        main_layout.addWidget(app_card)

        # --- Theme Card ---
        theme_card = QFrame()
        theme_card.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
            }
        """)
        theme_shadow = QGraphicsDropShadowEffect(self)
        theme_shadow.setBlurRadius(12)
        theme_shadow.setOffset(0, 4)
        theme_shadow.setColor(Qt.gray)
        theme_card.setGraphicsEffect(theme_shadow)
        theme_layout = QVBoxLayout(theme_card)
        theme_layout.setSpacing(14)
        theme_layout.setContentsMargins(18, 18, 18, 18)

        theme_title = QLabel("Giao diện")
        theme_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #406D96; border: none;")
        theme_layout.addWidget(theme_title)

        # Dark mode
        dark_mode_row = QHBoxLayout()
        dark_mode_label = QLabel("Chế độ tối")
        dark_mode_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; border: none;")
        self.dark_mode_switch = QSwitch()
        dark_mode_row.addWidget(dark_mode_label)
        dark_mode_row.addStretch()
        dark_mode_row.addWidget(self.dark_mode_switch)
        theme_layout.addLayout(dark_mode_row)

        main_layout.addWidget(theme_card)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Save button
        self.save_btn = QPushButton("Lưu cài đặt")
        self.save_btn.setStyleSheet("background: #406D96; color: white; font-size: 16px; border-radius: 8px; padding: 10px;")
        main_layout.addWidget(self.save_btn)

        # Back button
        self.back_btn = QPushButton("Quay lại")
        self.back_btn.setStyleSheet("color: #406D96; background: transparent; font-size: 14px;")
        main_layout.addWidget(self.back_btn)

    def _update_quality_label(self, value):
        self.quality_value_label.setText(f"{value}%")   