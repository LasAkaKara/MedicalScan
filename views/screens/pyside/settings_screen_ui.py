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

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QSlider, QCheckBox, QFileDialog, QMessageBox
from PySide6.QtCore import Qt

class SettingsScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(18)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("Cài đặt")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #002D40;")
        layout.addWidget(header)

        # Camera flip
        self.flip_h_checkbox = QCheckBox("Lật ngang camera")
        layout.addWidget(self.flip_h_checkbox)
        self.flip_v_checkbox = QCheckBox("Lật dọc camera")
        layout.addWidget(self.flip_v_checkbox)

        # Camera resolution
        res_layout = QHBoxLayout()
        res_label = QLabel("Độ phân giải camera:")
        self.res_combo = QComboBox()
        self.res_combo.addItems(["640x480", "800x600", "1280x720", "1920x1080"])
        res_layout.addWidget(res_label)
        res_layout.addWidget(self.res_combo)
        layout.addLayout(res_layout)

        # Camera quality
        qual_layout = QHBoxLayout()
        qual_label = QLabel("Chất lượng ảnh:")
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(10)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(80)
        qual_layout.addWidget(qual_label)
        qual_layout.addWidget(self.quality_slider)
        layout.addLayout(qual_layout)

        # Auto-detect and save original
        self.auto_detect_checkbox = QCheckBox("Tự động phát hiện tài liệu")
        layout.addWidget(self.auto_detect_checkbox)
        self.save_original_checkbox = QCheckBox("Lưu ảnh gốc")
        layout.addWidget(self.save_original_checkbox)

        # Theme
        self.dark_mode_checkbox = QCheckBox("Chế độ tối")
        layout.addWidget(self.dark_mode_checkbox)

        # Save button
        self.save_btn = QPushButton("Lưu cài đặt")
        self.save_btn.setStyleSheet("background: #406D96; color: white; font-size: 16px; border-radius: 8px; padding: 10px;")
        layout.addWidget(self.save_btn)

        # Back button
        self.back_btn = QPushButton("Quay lại")
        self.back_btn.setStyleSheet("color: #406D96; background: transparent; font-size: 14px;")
        layout.addWidget(self.back_btn)