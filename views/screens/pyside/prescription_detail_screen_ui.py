# #:import utils kivy.utils
# #:import dp kivy.metrics.dp

# <PrescriptionMedicineCard>:
#     size_hint_y: None
#     height: self.minimum_height
#     padding: dp(16)
#     spacing: dp(8)
#     radius: dp(12)
#     elevation: 2
#     md_bg_color: 1, 1, 1, 1
    
#     BoxLayout:
#         orientation: 'vertical'
#         spacing: dp(8)
#         size_hint_y: None
#         height: self.minimum_height
        
#         BoxLayout:
#             size_hint_y: None
#             height: self.minimum_height
#             spacing: dp(10)
            
#             MDIcon:
#                 icon: 'pill'
#                 size_hint: None, None
#                 size: dp(28), dp(28)
#                 color: utils.get_color_from_hex('#406D96')
#                 pos_hint: {'center_y': 0.5}
            
#             MDLabel:
#                 text: root.medicine_name
#                 font_style: 'H6'
#                 size_hint_y: None
#                 height: self.texture_size[1]
#                 bold: True
#                 theme_text_color: 'Primary'
        
#         BoxLayout:
#             orientation: 'vertical'
#             spacing: dp(4)
#             size_hint_y: None
#             height: self.minimum_height
#             padding: [dp(36), 0, 0, 0]
            
#             MDLabel:
#                 text: "Liều dùng"
#                 font_size: sp(13)
#                 font_name: 'Roboto'
#                 color: utils.get_color_from_hex('#667085')
#                 size_hint_y: None
#                 height: self.texture_size[1]
            
#             MDLabel:
#                 text: root.usage_info
#                 font_size: sp(16)
#                 font_name: 'Roboto'
#                 bold: True
#                 color: utils.get_color_from_hex('#344054')
#                 size_hint_y: None
#                 height: self.texture_size[1]
        
#         BoxLayout:
#             orientation: 'vertical'
#             spacing: dp(4)
#             size_hint_y: None
#             height: self.minimum_height
#             padding: [dp(36), 0, 0, 0]
            
#             MDLabel:
#                 text: "Tổng số lượng"
#                 font_size: sp(13)
#                 font_name: 'Roboto'
#                 color: utils.get_color_from_hex('#667085')
#                 size_hint_y: None
#                 height: self.texture_size[1]
            
#             MDLabel:
#                 text: f"{root.total_quantity} viên"
#                 font_size: sp(16)
#                 font_name: 'Roboto'
#                 bold: True
#                 color: utils.get_color_from_hex('#344054')
#                 size_hint_y: None
#                 height: self.texture_size[1]
        
#         BoxLayout:
#             orientation: 'vertical'
#             spacing: dp(4)
#             size_hint_y: None
#             height: self.minimum_height
#             padding: [dp(36), 0, 0, 0]
            
#             MDLabel:
#                 text: "Thời gian điều trị"
#                 font_size: sp(13)
#                 font_name: 'Roboto'
#                 color: utils.get_color_from_hex('#667085')
#                 size_hint_y: None
#                 height: self.texture_size[1]
            
#             MDLabel:
#                 text: root.duration
#                 font_size: sp(16)
#                 font_name: 'Roboto'
#                 bold: True
#                 color: utils.get_color_from_hex('#344054')
#                 size_hint_y: None
#                 height: self.texture_size[1]
        
#         BoxLayout:
#             orientation: 'vertical'
#             spacing: dp(4)
#             size_hint_y: None
#             height: self.minimum_height
#             padding: [dp(36), 0, 0, 0]
            
#             MDLabel:
#                 text: "Hướng dẫn sử dụng"
#                 font_size: sp(13)
#                 font_name: 'Roboto'
#                 color: utils.get_color_from_hex('#667085')
#                 size_hint_y: None
#                 height: self.texture_size[1]
            
#             MDLabel:
#                 text: root.usage_instruction
#                 font_size: sp(15)
#                 font_name: 'Roboto'
#                 color: utils.get_color_from_hex('#344054')
#                 size_hint_y: None
#                 height: self.texture_size[1]
#                 text_size: self.width, None

# <PrescriptionDetailScreen>:
#     BoxLayout:
#         orientation: 'vertical'
#         spacing: dp(16)
#         padding: dp(16)
        
#         MDTopAppBar:
#             title: "Chi tiết đơn thuốc"
#             left_action_items: [['arrow-left', lambda x: root.go_back()]]
#             right_action_items: [['printer', lambda x: root.print_prescription()], ['share', lambda x: root.share_prescription()]]
#             elevation: 0
#             md_bg_color: app.theme_cls.primary_color
        
#         ScrollView:
#             BoxLayout:
#                 orientation: 'vertical'
#                 spacing: dp(16)
#                 size_hint_y: None
#                 height: self.minimum_height
#                 padding: dp(16)
                
#                 MDCard:
#                     size_hint_y: None
#                     height: dp(120)
#                     padding: dp(16)
#                     spacing: dp(8)
#                     radius: dp(12)
#                     elevation: 2
                    
#                     BoxLayout:
#                         orientation: 'vertical'
#                         spacing: dp(8)
#                         pos_hint: {'center_y': 0.5}
                        
#                         MDLabel:
#                             id: prescription_name
#                             text: ""
#                             font_style: 'H5'
#                             size_hint_y: None
#                             height: self.texture_size[1]
#                             bold: True
#                             theme_text_color: 'Primary'
#                             halign: 'center'
#                             valign: 'middle'
#                             pos_hint: {'center_x': 0.5, 'center_y': 0.5}
#                             text_size: self.width, None
                        
#                         MDLabel:
#                             id: hospital_name
#                             text: ""
#                             font_style: 'Body1'
#                             size_hint_y: None
#                             height: self.texture_size[1]
#                             theme_text_color: 'Secondary'
                        
#                         MDLabel:
#                             id: created_date
#                             text: ""
#                             font_style: 'Body1'
#                             size_hint_y: None
#                             height: self.texture_size[1]
#                             theme_text_color: 'Secondary'
                        
#                         MDChip:
#                             id: status_chip
#                             text: ""
#                             icon: "check-circle"
#                             size_hint: None, None
#                             size: dp(120), dp(32)
#                             pos_hint: {'center_x': 0.5}
                
#                 MDLabel:
#                     text: "Danh sách thuốc"
#                     font_style: 'H6'
#                     size_hint_y: None
#                     height: self.texture_size[1]
#                     bold: True
#                     theme_text_color: 'Primary'
#                     padding: [0, dp(8), 0, dp(8)]
                
#                 BoxLayout:
#                     id: medicines_layout
#                     orientation: 'vertical'
#                     spacing: dp(16)
#                     size_hint_y: None
#                     height: self.minimum_height 

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea, QFrame
from PySide6.QtCore import Qt

class PrescriptionMedicineCard(QFrame):
    def __init__(self, medicine, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background: #fff; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 12px;")
        layout = QVBoxLayout(self)
        name = QLabel(medicine.get('medicine_name', ''))
        name.setStyleSheet("font-size: 17px; font-weight: bold; color: #344054;")
        layout.addWidget(name)
        usage = QLabel(f"Liều dùng: {medicine.get('quantity_per_time', '')} viên/lần, {', '.join(medicine.get('usage_time', []))}")
        usage.setStyleSheet("font-size: 14px; color: #406D96;")
        layout.addWidget(usage)
        total = QLabel(f"Tổng số lượng: {medicine.get('total_quantity', '')} viên")
        total.setStyleSheet("font-size: 14px; color: #406D96;")
        layout.addWidget(total)
        duration = QLabel(f"Thời gian điều trị: {medicine.get('duration_days', '')} ngày")
        duration.setStyleSheet("font-size: 14px; color: #406D96;")
        layout.addWidget(duration)
        instruction = QLabel(f"Hướng dẫn sử dụng: {medicine.get('usage_instruction', '')}")
        instruction.setStyleSheet("font-size: 14px; color: #344054;")
        instruction.setWordWrap(True)
        layout.addWidget(instruction)

class PrescriptionDetailScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # Top bar
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("←")
        self.back_btn.setFixedSize(36, 36)
        self.back_btn.setStyleSheet("font-size: 18px; border-radius: 18px; background: #e3eaf6;")
        top_bar.addWidget(self.back_btn)
        title = QLabel("Chi tiết đơn thuốc")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #002D40;")
        top_bar.addWidget(title)
        top_bar.addStretch()
        self.print_btn = QPushButton("In")
        self.share_btn = QPushButton("Chia sẻ")
        top_bar.addWidget(self.print_btn)
        top_bar.addWidget(self.share_btn)
        main_layout.addLayout(top_bar)

        # Prescription info
        self.prescription_name = QLabel("")
        self.prescription_name.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(self.prescription_name)
        self.hospital_name = QLabel("")
        self.hospital_name.setStyleSheet("font-size: 14px; color: #406D96;")
        main_layout.addWidget(self.hospital_name)
        self.created_date = QLabel("")
        self.created_date.setStyleSheet("font-size: 14px; color: #406D96;")
        main_layout.addWidget(self.created_date)
        self.status_chip = QLabel("")
        self.status_chip.setStyleSheet("font-size: 13px; border-radius: 8px; padding: 4px 12px; background: #ECFDF3; color: #12B76A;")
        main_layout.addWidget(self.status_chip)

        # Medicines list
        main_layout.addWidget(QLabel("Danh sách thuốc:"))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.medicines_container = QWidget()
        self.medicines_layout = QVBoxLayout(self.medicines_container)
        self.medicines_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.medicines_container)
        main_layout.addWidget(self.scroll_area)