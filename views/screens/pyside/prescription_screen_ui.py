# #:import utils kivy.utils
# #:import MDCard kivymd.uix.card
# #:import dp kivy.metrics.dp
# #:import Animation kivy.animation.Animation

# <MedicineDetailCard@MDCard>:
#     orientation: 'vertical'
#     size_hint_y: None
#     height: self.minimum_height
#     md_bg_color: utils.get_color_from_hex('#FFFFFF')
#     radius: [16]
#     elevation: 0
#     padding: [dp(18), dp(14)]
#     spacing: dp(10)

#     canvas.before:
#         Color:
#             rgba: utils.get_color_from_hex('#F8FAFC')
#         RoundedRectangle:
#             pos: self.pos
#             size: self.size
#             radius: [16]

#     # Medicine Name Header
#     BoxLayout:
#         size_hint_y: None
#         height: self.minimum_height
#         spacing: dp(10)

#         MDIcon:
#             icon: 'pill'
#             size_hint: None, None
#             size: dp(28), dp(28)
#             color: utils.get_color_from_hex('#406D96')
#             pos_hint: {'center_y': 0.5}

#         MDLabel:
#             text: root.medicine_name
#             font_size: sp(18)
#             font_name: 'Roboto'
#             bold: True
#             color: utils.get_color_from_hex('#344054')
#             size_hint_y: None
#             height: self.texture_size[1]

#     # Medicine Details
#     BoxLayout:
#         orientation: 'vertical'
#         spacing: dp(8)
#         size_hint_y: None
#         height: self.minimum_height
#         padding: [dp(36), 0, 0, 0]

#         # Dosage Row
#         BoxLayout:
#             orientation: 'vertical'
#             spacing: dp(4)
#             size_hint_y: None
#             height: self.minimum_height

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

#         # Total Quantity Row
#         BoxLayout:
#             orientation: 'vertical'
#             spacing: dp(4)
#             size_hint_y: None
#             height: self.minimum_height

#             MDLabel:
#                 text: "Tổng số lượng"
#                 font_size: sp(13)
#                 font_name: 'Roboto'
#                 color: utils.get_color_from_hex('#667085')
#                 size_hint_y: None
#                 height: self.texture_size[1]

#             MDLabel:
#                 text: root.total_quantity + " viên"
#                 font_size: sp(16)
#                 font_name: 'Roboto'
#                 bold: True
#                 color: utils.get_color_from_hex('#344054')
#                 size_hint_y: None
#                 height: self.texture_size[1]

#         # Duration Row
#         BoxLayout:
#             orientation: 'vertical'
#             spacing: dp(4)
#             size_hint_y: None
#             height: self.minimum_height

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

#         # Instructions Row
#         BoxLayout:
#             orientation: 'vertical'
#             spacing: dp(4)
#             size_hint_y: None
#             height: self.minimum_height

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

# <PrescriptionCard>:
#     orientation: 'vertical'
#     size_hint_y: None
#     height: main_content.height + (details_content.height if root.show_details else 0) + dp(42)
#     md_bg_color: utils.get_color_from_hex('#FFFFFF')
#     radius: [20]
#     elevation: 2
#     padding: [dp(18), dp(14), dp(18), dp(14)]
#     spacing: dp(6)
#     ripple_behavior: True
#     show_details: False

#     canvas.before:
#         Color:
#             rgba: utils.get_color_from_hex('#FFFFFF')
#         RoundedRectangle:
#             pos: self.pos
#             size: self.size
#             radius: [20]
        
#         # Left accent
#         Color:
#             rgba: utils.get_color_from_hex('#406D96')
#         RoundedRectangle:
#             pos: self.pos[0], self.pos[1]
#             size: dp(4), self.height
#             radius: [(2, 2), (2, 2), (2, 2), (2, 2)]

#     # Main Content Container
#     BoxLayout:
#         id: main_content
#         orientation: 'vertical'
#         spacing: dp(6)
#         size_hint_y: None
#         height: self.minimum_height
#         pos_hint: {'center_x': 0.5}

#         # Info Rows Container
#         BoxLayout:
#             orientation: 'vertical'
#             size_hint_y: None
#             height: self.minimum_height
#             spacing: dp(6)
#             padding: [0, 0, 0, 0]
#             pos_hint: {'center_x': 0.5}

#             # Title Row
#             BoxLayout:
#                 size_hint_y: None
#                 height: dp(36)
#                 spacing: dp(10)
#                 pos_hint: {'center_x': 0.5, 'center_y': 0.5}

#                 MDIcon:
#                     icon: 'file-document-outline'
#                     size_hint: None, None
#                     size: dp(24), dp(24)
#                     color: utils.get_color_from_hex('#344054')
#                     pos_hint: {'center_y': 0.5}

#                 MDLabel:
#                     text: root.title if root.title else ''
#                     font_size: sp(17)
#                     font_name: 'Roboto'
#                     bold: True
#                     color: utils.get_color_from_hex('#344054')
#                     size_hint_y: None
#                     height: dp(36)
#                     valign: 'middle'
#                     text_size: self.width, None
#                     shorten: True
#                     shorten_from: 'right'
#                     halign: 'center'
#                     size_hint_x: 1
#                     pos_hint: {'center_x': 0.5, 'center_y': 0.5}

#             # Hospital Row
#             BoxLayout:
#                 size_hint_y: None
#                 height: dp(32)
#                 spacing: dp(12)
#                 pos_hint: {'center_x': 0.5}

#                 MDIcon:
#                     icon: 'hospital-building'
#                     size_hint: None, None
#                     size: dp(20), dp(20)
#                     color: utils.get_color_from_hex('#667085')
#                     pos_hint: {'center_y': 0.5}

#                 MDLabel:
#                     text: root.hospital if root.hospital else ''
#                     font_size: sp(14)
#                     font_name: 'Roboto'
#                     color: utils.get_color_from_hex('#667085')
#                     size_hint_y: None
#                     height: dp(32)
#                     valign: 'middle'
#                     text_size: self.width, None
#                     shorten: True
#                     shorten_from: 'right'
#                     halign: 'left'
#                     size_hint_x: 1

#             # Date Row
#             BoxLayout:
#                 size_hint_y: None
#                 height: dp(32)
#                 spacing: dp(12)
#                 pos_hint: {'center_x': 0.5}

#                 MDIcon:
#                     icon: 'calendar'
#                     size_hint: None, None
#                     size: dp(20), dp(20)
#                     color: utils.get_color_from_hex('#667085')
#                     pos_hint: {'center_y': 0.5}

#                 MDLabel:
#                     text: root.date if root.date else ''
#                     font_size: sp(14)
#                     font_name: 'Roboto'
#                     color: utils.get_color_from_hex('#667085')
#                     size_hint_y: None
#                     height: dp(32)
#                     valign: 'middle'
#                     text_size: self.width, None
#                     shorten: True
#                     shorten_from: 'right'
#                     halign: 'left'
#                     size_hint_x: 1

#             # Category Row
#             BoxLayout:
#                 size_hint_y: None
#                 height: dp(32)
#                 spacing: dp(12)
#                 pos_hint: {'center_x': 0.5}

#                 MDIcon:
#                     icon: 'tag'
#                     size_hint: None, None
#                     size: dp(20), dp(20)
#                     color: utils.get_color_from_hex('#667085')
#                     pos_hint: {'center_y': 0.5}

#                 MDLabel:
#                     text: root.category if root.category else ''
#                     font_size: sp(14)
#                     font_name: 'Roboto'
#                     color: root.category_text_color
#                     size_hint_y: None
#                     height: dp(32)
#                     valign: 'middle'
#                     text_size: self.width, None
#                     shorten: True
#                     shorten_from: 'right'
#                     halign: 'left'
#                     size_hint_x: 1

#     # Expandable Details Section
#     BoxLayout:
#         id: details_content
#         orientation: 'vertical'
#         size_hint_y: None
#         height: self.minimum_height if root.show_details else 0
#         opacity: 1 if root.show_details else 0
#         spacing: dp(12)
#         padding: [dp(8), dp(16), dp(8), dp(16)]
#         pos_hint: {'center_x': 0.5}

#         canvas.before:
#             Color:
#                 rgba: utils.get_color_from_hex('#F8FAFC')
#             RoundedRectangle:
#                 pos: self.pos
#                 size: self.size
#                 radius: [0, 0, 20, 20]

#         BoxLayout:
#             size_hint_y: None
#             height: dp(28)
#             spacing: dp(10)
#             pos_hint: {'center_x': 0.5}

#             MDIcon:
#                 icon: 'format-list-bulleted'
#                 size_hint: None, None
#                 size: dp(20), dp(20)
#                 color: utils.get_color_from_hex('#406D96')
#                 pos_hint: {'center_y': 0.5}

#             MDLabel:
#                 text: 'Danh sách thuốc'
#                 font_size: sp(15)
#                 font_name: 'Roboto'
#                 bold: True
#                 color: utils.get_color_from_hex('#344054')
#                 size_hint_y: None
#                 height: dp(28)
#                 valign: 'middle'
#                 halign: 'center'

#         BoxLayout:
#             id: medicines_list
#             orientation: 'vertical'
#             size_hint_y: None
#             height: self.minimum_height
#             spacing: dp(10)
#             padding: [dp(8), 0, 0, 0]

# <HistoryScreen>:
#     BoxLayout:
#         orientation: 'vertical'

#         # Header
#         Header:
#         # BoxLayout:
#         #     size_hint_y: None
#         #     height: dp(140)
#         #     padding: [dp(20), dp(20)]
#         #     spacing: dp(12)
#         #     canvas.before:
#         #         Color:
#         #             rgba: utils.get_color_from_hex('#FFFFFF')
#         #         Rectangle:
#         #             pos: self.pos
#         #             size: self.size
#         #         Color:
#         #             rgba: utils.get_color_from_hex('#F5F8FF')
#         #         Rectangle:
#         #             pos: self.pos[0], self.pos[1]
#         #             size: self.width, dp(4)

#         #     MDIconButton:
#         #         icon: 'arrow-left'
#         #         size_hint: None, None
#         #         size: dp(48), dp(48)
#         #         pos_hint: {'center_y': 0.5}
#         #         theme_text_color: "Custom"
#         #         text_color: utils.get_color_from_hex('#406D96')
#         #         md_bg_color: utils.get_color_from_hex('#F1F9FF')
#         #         on_release: app.root.switch_screen("medical_home")

#         #     BoxLayout:
#         #         orientation: 'vertical'
#         #         spacing: dp(6)
#         #         padding: [0, dp(12)]

#         #         MDLabel:
#         #             text: 'Đơn thuốc'
#         #             font_size: sp(38)
#         #             font_name: 'Roboto'
#         #             bold: True
#         #             color: utils.get_color_from_hex('#002D40')

#         #         MDLabel:
#         #             text: 'Quản lý các đơn thuốc của bạn tại đây'
#         #             font_size: sp(16)
#         #             font_name: 'Roboto'
#         #             color: utils.get_color_from_hex('#667085')

#         #     MDIconButton:
#         #         icon: 'bell'
#         #         size_hint: None, None
#         #         size: dp(52), dp(52)
#         #         md_bg_color: utils.get_color_from_hex('#F1F9FF')
#         #         theme_text_color: "Custom"
#         #         text_color: utils.get_color_from_hex('#406D96')
#         #         pos_hint: {'center_y': 0.5}

#         # Search Box
#         BoxLayout:
#             size_hint_y: None
#             height: dp(80)
#             padding: [dp(16), dp(8)]
#             # canvas.before:
#             #     Color:
#             #         rgba: utils.get_color_from_hex('#FFFFFF')
#             #     Rectangle:
#             #         pos: self.pos
#             #         size: self.size
#             #     Color:
#             #         rgba: utils.get_color_from_hex('#F0F0F0')
#             #     Rectangle:
#             #         pos: self.pos[0], self.pos[1] + self.height - dp(1)
#             #         size: self.width, dp(1)

#             MDCard:
#                 radius: [20]
#                 elevation: 0
#                 padding: [dp(18), 0]

#                 BoxLayout:
#                     spacing: dp(14)
#                     padding: [dp(8), 0]

#                     MDIcon:
#                         icon: 'magnify'
#                         size_hint: None, None
#                         size: dp(28), dp(28)
#                         pos_hint: {'center_y': 0.5}

#                     TextInput:
#                         id: search_input
#                         hint_text: 'Tìm kiếm đơn thuốc...'
#                         background_color: 0, 0, 0, 0
#                         font_size: sp(17)
#                         font_name: 'Roboto'
#                         multiline: False
#                         hint_text_color: utils.get_color_from_hex('#98A2B3')
#                         foreground_color: utils.get_color_from_hex('#344054')
#                         padding: [0, dp(10), 0, dp(10)]
#                         valign: 'center'
#                         halign: 'left'
#                         pos_hint: {'center_y': 0.5}
#                         on_text: root.search_prescriptions(self.text)

#         # "All" Label
#         BoxLayout:
#             size_hint_y: None
#             height: dp(60)
#             padding: [dp(20), dp(12)]
            
#             MDLabel:
#                 text: 'Tất cả đơn thuốc'
#                 font_size: sp(22)
#                 font_name: 'Roboto'
#                 bold: True

#         # Prescriptions List
#         ScrollView:
#             do_scroll_x: False
#             bar_width: dp(4)
#             bar_color: utils.get_color_from_hex('#E4E7EC')
#             bar_inactive_color: utils.get_color_from_hex('#E4E7EC')

#             BoxLayout:
#                 id: prescriptions_layout
#                 orientation: 'vertical'
#                 size_hint_y: None
#                 height: self.minimum_height
#                 padding: [dp(16), dp(16), dp(16), dp(16)]
#                 spacing: dp(24)

#         # Add Button
#         FloatLayout:
#             size_hint_y: None
#             height: dp(80)
#             MDFloatingActionButton:
#                 icon: 'plus'
#                 user_font_size: sp(24)
#                 size_hint: None, None
#                 size: dp(64), dp(64)
#                 elevation: 4
#                 pos_hint: {'right': 0.96, 'y': 0.2}
#                 on_press: root.add_prescription()

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea, QFrame, QLineEdit, QSizePolicy
from PySide6.QtCore import Qt

class PrescriptionCard(QFrame):
    def __init__(self, title, category, category_color, category_text_color, date, hospital, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            background: #fff;
            border-radius: 16px;
            border: 1px solid #e0e0e0;
            margin-bottom: 12px;
        """)
        layout = QVBoxLayout(self)
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 17px; font-weight: bold; color: #344054;")
        layout.addWidget(title_label)
        info_label = QLabel(f"{hospital} | {date} | {category}")
        info_label.setStyleSheet(f"font-size: 13px; color: {category_text_color};")
        layout.addWidget(info_label)

class PrescriptionScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)

        header = QLabel("Tất cả đơn thuốc")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #002D40;")
        main_layout.addWidget(header)

        # Search box
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm đơn thuốc...")
        self.search_input.setStyleSheet("font-size: 16px; padding: 8px; border-radius: 8px; border: 1px solid #e0e0e0;")
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Scroll area for prescriptions
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.prescriptions_container = QWidget()
        self.prescriptions_layout = QVBoxLayout(self.prescriptions_container)
        self.prescriptions_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.prescriptions_container)
        main_layout.addWidget(self.scroll_area)

        # Add button
        self.add_btn = QPushButton("Thêm đơn thuốc")
        self.add_btn.setStyleSheet("background: #406D96; color: white; font-size: 16px; border-radius: 8px; padding: 10px;")
        main_layout.addWidget(self.add_btn)
