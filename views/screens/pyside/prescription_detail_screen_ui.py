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

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea, QFrame, QGridLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize
from themes import PRIMARY_COLOR, TEXT_COLOR, HINT_COLOR, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG, FONT_FAMILY
from PySide6.QtGui import QIcon

class PrescriptionMedicineCard(QFrame):
    def __init__(self, medicine, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"background: #fff; border-radius: 12px; margin-bottom: 12px; font-family: {FONT_FAMILY};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

        # Medicine name
        name = QLabel(medicine.get('medicine_name', ''))
        name.setStyleSheet("font-size: 17px; font-weight: bold; color: #344054;")
        layout.addWidget(name)

        # Helper for bold label + value
        def add_info_row(label_text, value_text):
            row = QHBoxLayout()
            row.setSpacing(6)
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: #406D96;")
            value = QLabel(value_text)
            value.setStyleSheet("font-size: 14px; color: #344054;")
            value.setWordWrap(True)
            row.addWidget(label)
            row.addWidget(value, 1)
            layout.addLayout(row)

        # Usage times (Sáng, Trưa, Tối) as a wrapped label
        usage_times = medicine.get('usage_time', [])
        if usage_times and isinstance(usage_times[0], dict):
            usage_str = ", ".join(f"{t['time']} ({t['quantity']})" for t in usage_times)
        else:
            usage_str = ", ".join(usage_times)
        add_info_row("Thời điểm:", usage_str)
        add_info_row("Liều dùng:", medicine.get('quantity_per_time', ''))
        add_info_row("Tổng số lượng:", medicine.get('total_quantity', ''))
        add_info_row("Thời gian điều trị:", medicine.get('duration_days', ''))
        add_info_row("Hướng dẫn sử dụng:", medicine.get('usage_instruction', ''))

class PrescriptionDetailScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- Main scroll area for the whole screen ---
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 4px 2px 4px 0px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #D0D5DD;
                min-height: 36px;
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
                border: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)

        # --- Content widget inside scroll area ---
        content = QWidget()
        scroll.setWidget(content)
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(16, 16, 16, 16)

        # Top bar
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton()
        self.back_btn.setFixedSize(36, 36)
        self.back_btn.setIcon(QIcon("assets/back.png"))
        self.back_btn.setIconSize(QSize(28, 28))
        self.back_btn.setStyleSheet("background: transparent;")
        top_bar.addWidget(self.back_btn)
        title = QLabel("Chi tiết đơn thuốc")
        title.setStyleSheet(f"font-size: {FONT_SIZE_LG}px; font-weight: bold; color: #002D40;")
        top_bar.addWidget(title)
        self.main_layout.addLayout(top_bar)


        # --- Patient info section label ---
        patient_section_label = QLabel("Thông tin bệnh nhân")
        patient_section_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: #406D96; margin-bottom: 6px; font-family: {FONT_FAMILY}")
        self.main_layout.addWidget(patient_section_label, alignment=Qt.AlignLeft)

        # --- Patient info card (vertical layout, reduced width, wrap values) ---
        patient_card = QFrame()
        patient_card.setStyleSheet("""
            background: #fff; 
            border-radius: 12px; 
        """)
        patient_card.setFixedWidth(360)

        # Add drop shadow
        shadow = QGraphicsDropShadowEffect(patient_card)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(Qt.gray)
        patient_card.setGraphicsEffect(shadow)

        patient_layout = QVBoxLayout(patient_card)
        patient_layout.setContentsMargins(20, 16, 20, 16)
        patient_layout.setSpacing(10)

        label_style = f"font-size: 16px; font-weight: bold; color: {TEXT_COLOR}; font-family: {FONT_FAMILY}"
        value_style = f"font-size: 16px; color: {TEXT_COLOR}; font-family: {FONT_FAMILY}"

        self.patient_name = QLabel()
        self.doctor_name = QLabel()
        self.age = QLabel()
        self.weight = QLabel()
        self.gender = QLabel()
        self.diagnosis = QLabel()
        self.created_date = QLabel()
        self.hospital_name = QLabel()
        self.category_name = QLabel()

        for lbl in [
            self.patient_name, self.doctor_name, self.age, self.weight,
            self.gender, self.diagnosis, self.created_date, self.hospital_name, self.category_name
        ]:
            lbl.setWordWrap(True)
            lbl.setMinimumWidth(120)
            lbl.setMaximumWidth(260)

        def add_row(label, value_widget):
            row = QHBoxLayout()
            row.setSpacing(12)
            row.addWidget(self._styled_label(label, label_style))
            row.addWidget(self._styled_label_widget(value_widget, value_style), 1)
            row.addStretch()
            patient_layout.addLayout(row)

        add_row("Bệnh nhân:", self.patient_name)
        add_row("Bác sĩ:", self.doctor_name)
        add_row("Tuổi:", self.age)
        add_row("Cân nặng:", self.weight)
        add_row("Giới tính:", self.gender)
        add_row("Chẩn đoán:", self.diagnosis)
        add_row("Ngày tạo:", self.created_date)
        add_row("Bệnh viện:", self.hospital_name)
        add_row("Loại đơn:", self.category_name)

        self.main_layout.addWidget(patient_card, alignment=Qt.AlignLeft)

        # --- Medicines list label (larger, bold) ---
        med_list_label = QLabel("Danh sách thuốc")
        med_list_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: #406D96; margin-top: 12px; margin-bottom: 6px; font-family: {FONT_FAMILY}")
        self.main_layout.addWidget(med_list_label, alignment=Qt.AlignLeft)

        # --- Medicines list ---
        self.medicines_container = QWidget()
        self.medicines_layout = QVBoxLayout(self.medicines_container)
        self.medicines_layout.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(self.medicines_container)

    def _styled_label(self, text, style):
        lbl = QLabel(text)
        lbl.setStyleSheet(style)
        return lbl

    def _styled_label_widget(self, widget, style):
        widget.setStyleSheet(style)
        return widget

    def set_prescription(self, prescription):
        self.patient_name.setText(prescription.get('patient_name', ''))
        self.doctor_name.setText(prescription.get('doctor_name', ''))
        self.age.setText(str(prescription.get('age', '')))
        self.weight.setText(str(prescription.get('weight', '')))
        self.gender.setText(prescription.get('gender', ''))
        self.diagnosis.setText(prescription.get('diagnosis', ''))
        self.created_date.setText(prescription.get('created_at', ''))
        self.hospital_name.setText(prescription.get('hospital_name', ''))
        self.category_name.setText(prescription.get('category_name', ''))

        # Clear old medicines
        for i in reversed(range(self.medicines_layout.count())):
            widget = self.medicines_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Add new medicines
        for med in prescription.get('medicines', []):
            card = PrescriptionMedicineCard(med)
            self.medicines_layout.addWidget(card)