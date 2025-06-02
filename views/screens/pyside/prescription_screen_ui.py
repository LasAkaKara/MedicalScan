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

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea, QFrame,
    QLineEdit, QSizePolicy, QToolButton, QGridLayout, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QSize
from themes import PRIMARY_COLOR, FONT_SIZE_MD, FONT_SIZE_XL, HINT_COLOR, FONT_FAMILY

class MedicineRow(QFrame):
    def __init__(self, name, med_type, quantity, times, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            background: #FCFCFD;
            border-radius: 8px;
            border: 1px solid #EAECF0;
            font-family: Roboto, sans-serif;
        """)

        main_layout = QGridLayout(self)
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setHorizontalSpacing(8)
        main_layout.setVerticalSpacing(2)

        # --- Top row ---
        name_label = QLabel(name)
        name_label.setStyleSheet(f"font-size: {FONT_SIZE_MD}px; font-weight: bold; color: #344054; border: none;")
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        main_layout.addWidget(name_label, 0, 0, 1, 6, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        # Loại
        type_desc = QLabel("Loại:")
        type_desc.setStyleSheet("font-size: 13px; color: #667085; font-weight: 600; border: none;")
        type_desc.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(type_desc, 1, 0, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        type_value = QLabel(med_type)
        type_value.setStyleSheet("font-size: 13px; color: #406D96; font-weight: bold; border: none;")
        type_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        main_layout.addWidget(type_value, 1, 1, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        # Sáng
        sang_desc = QLabel("Sáng:")
        sang_desc.setStyleSheet("font-size: 13px; color: #667085; font-weight: 600; border: none;")
        sang_desc.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(sang_desc, 1, 2, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        sang_val = QLabel("1" if "Sáng" in times else "0")
        sang_val.setStyleSheet("font-size: 13px; color: #406D96; font-weight: bold; border: none;")
        sang_val.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(sang_val, 1, 3, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        # Trưa
        trua_desc = QLabel("Trưa:")
        trua_desc.setStyleSheet("font-size: 13px; color: #667085; font-weight: 600; border: none;")
        trua_desc.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(trua_desc, 1, 4, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        trua_val = QLabel("1" if "Trưa" in times else "0")
        trua_val.setStyleSheet("font-size: 13px; color: #406D96; font-weight: bold; border: none;")
        trua_val.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(trua_val, 1, 5, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        # Tối
        toi_desc = QLabel("Tối:")
        toi_desc.setStyleSheet("font-size: 13px; color: #667085; font-weight: 600; border: none;")
        toi_desc.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(toi_desc, 1, 6, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        toi_val = QLabel("1" if "Tối" in times else "0")
        toi_val.setStyleSheet("font-size: 13px; color: #406D96; font-weight: bold; border: none;")
        toi_val.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(toi_val, 1, 7, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        # SL (quantity) and edit icon in the last column, spanning both rows
        qty_desc = QLabel("SL:")
        qty_desc.setStyleSheet("font-size: 13px; color: #667085; font-weight: 600; border: none;")
        qty_desc.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(qty_desc, 0, 6, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignRight)

        qty_label = QLabel(str(quantity))
        qty_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #406D96; border: none;")
        qty_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(qty_label, 0, 7, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        self.edit_btn = QToolButton()
        self.edit_btn.setIcon(QIcon("assets/edit.png"))
        self.edit_btn.setStyleSheet("border: none;")
        self.edit_btn.setToolTip("Chỉnh sửa thuốc")
        self.edit_btn.setIconSize(QSize(24, 24))
        self.edit_btn.setFixedSize(32, 48)
        main_layout.addWidget(self.edit_btn, 0, 8, 2, 1, alignment=Qt.AlignVCenter | Qt.AlignRight)

class PrescriptionCard(QFrame):
    def __init__(self, prescription, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)  # No border for the card container
        self.setFixedWidth(360)  # Set a smaller fixed width for the card
        self.setStyleSheet(f"""
            background: #fff;
            border-radius: 16px;
            border: none;
            margin-bottom: 12px;
            font-family: {FONT_FAMILY};
        """)
        self.expanded = False
        self.prescription = prescription

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 12)

        # Box shadow effect for the card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

        # Top row: Title and expand/collapse
        top_row = QHBoxLayout()
        top_row.setSpacing(0)
        title_label = QLabel(prescription.get('name', 'Không có tên'))
        title_label.setStyleSheet(f"font-size: 17px; font-weight: bold; color: #344054; font-family: {FONT_FAMILY};")
        top_row.addWidget(title_label)
        top_row.addStretch()

        # Expand/collapse button with custom image
        self.expand_btn = QToolButton()
        self.expand_btn.setIcon(QIcon("assets/down-arrow.png"))
        self.expand_btn.setCheckable(True)
        self.expand_btn.setChecked(False)
        self.expand_btn.clicked.connect(self.toggle_expand)
        self.expand_btn.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            border: none;
            padding: 0px;
        """)
        self.expand_btn.setIconSize(QSize(32, 32))
        self.expand_btn.setFixedSize(40, 40)
        top_row.addWidget(self.expand_btn, alignment=Qt.AlignVCenter)
        self.main_layout.addLayout(top_row)

        # Category tag below the title (fit text width)
        category = prescription.get('category_name', 'Không phân loại')
        tag_row = QHBoxLayout()
        tag_row.setContentsMargins(0, 0, 0, 0)
        tag_row.setSpacing(0)

        # Category tag with icon inside (icon left, text right)
        tag_widget = QWidget()
        tag_layout = QHBoxLayout(tag_widget)
        tag_layout.setContentsMargins(8, 0, 8, 0)  # padding left/right for pill look
        tag_layout.setSpacing(6)

        icon_label = QLabel()
        icon_label.setPixmap(QIcon("assets/price-tag-yellow.png").pixmap(32, 32))
        icon_label.setFixedSize(22, 32)
        tag_layout.addWidget(icon_label)

        tag = QLabel(category)
        tag.setStyleSheet(f"""
            font-size: 12px;
            color: #887A05;
            background: transparent;
            font-family: {FONT_FAMILY};
        """)
        tag_layout.addWidget(tag)

        tag_widget.setStyleSheet(f"""
            background: #F2F3DA;
            border-radius: 8px;
            min-width: 0px;
            max-width: 1000px;
            margin-top: 2px;
        """)
        tag_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        tag_widget.setMaximumWidth(tag.fontMetrics().horizontalAdvance(category) + 16 + 24)  # icon + padding

        tag_row.addWidget(tag_widget)
        tag_row.addStretch()
        tag_row_widget = QWidget()
        tag_row_widget.setLayout(tag_row)
        # Reduce the vertical space between name and category
        self.main_layout.addWidget(tag_row_widget, alignment=Qt.AlignLeft)
        self.main_layout.setSpacing(2)  # Even smaller spacing between rows

        # Info row: date and hospital
        info_row = QHBoxLayout()
        # Date icon
        date_icon_label = QLabel()
        date_icon_label.setPixmap(QIcon("assets/calendar-small.png").pixmap(32, 32))
        date_icon_label.setFixedSize(20, 32)
        date_icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        info_row.addWidget(date_icon_label)
        # Date text
        date_label = QLabel(prescription.get('created_at', ''))
        date_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: #667085; font-family: {FONT_FAMILY};")
        info_row.addWidget(date_label)
        # Hospital icon
        hospital_icon_label = QLabel()
        hospital_icon_label.setPixmap(QIcon("assets/hospital.png").pixmap(32, 32))
        hospital_icon_label.setFixedSize(20, 32)
        hospital_icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        info_row.addWidget(hospital_icon_label)
        # Hospital text
        hospital_label = QLabel(prescription.get('hospital_name', ''))
        hospital_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: #667085; margin-left: 6px; font-family: {FONT_FAMILY};")
        info_row.addWidget(hospital_label)
        info_row.addStretch()
        self.main_layout.addLayout(info_row)

        # Expandable medicine list
        self.meds_widget = QWidget()
        self.meds_layout = QVBoxLayout(self.meds_widget)
        self.meds_layout.setContentsMargins(8, 4, 8, 4)
        self.meds_layout.setSpacing(4)
        self.meds_widget.setVisible(False)
        # Add medicine rows if any
        for med in prescription.get('medicines', []):
            med_row = MedicineRow(
                name=med.get('medicine_name', ''),
                med_type=med.get('type', ''),
                quantity=med.get('quantity_per_time', ''),
                times=med.get('usage_time', []),
            )
            # Set font family for all QLabel children in MedicineRow
            for child in med_row.findChildren(QLabel):
                child.setStyleSheet(child.styleSheet() + f"font-family: {FONT_FAMILY};")
            med_row.setStyleSheet(med_row.styleSheet() + f"font-family: {FONT_FAMILY};")
            self.meds_layout.addWidget(med_row)
        self.main_layout.addWidget(self.meds_widget)

    def toggle_expand(self):
        self.expanded = not self.expanded
        self.meds_widget.setVisible(self.expanded)
        if self.expanded:
            self.expand_btn.setIcon(QIcon("assets/up-arrow.png"))
        else:
            self.expand_btn.setIcon(QIcon("assets/down-arrow.png"))

class PrescriptionScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        MAIN_MARGIN = 16  # Set your desired margin here

        # Outer layout for margin, inner layout for content (no margin)
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignTop)
        outer_layout.setSpacing(0)
        outer_layout.setContentsMargins(MAIN_MARGIN, 0, MAIN_MARGIN, 0)  # Only this layout has margin

        # Inner widget and layout (no margin, so shadow is not clipped)
        inner_widget = QWidget()
        inner_layout = QVBoxLayout(inner_widget)
        inner_layout.setAlignment(Qt.AlignTop)
        inner_layout.setSpacing(0)
        inner_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QFrame()
        header.setStyleSheet("background: #fff;")
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(0)

        # Top row: back, title+subtitle, bell (centered)
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(0)

        self.back_btn = QToolButton()
        self.back_btn.setIcon(QIcon("assets/back.png"))
        self.back_btn.setIconSize(QSize(28, 28))
        self.back_btn.setFixedSize(36, 36)
        self.back_btn.setStyleSheet("background: transparent;")
        top_row.addWidget(self.back_btn, alignment=Qt.AlignVCenter)

        # Center widget for title and subtitle
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        center_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Đơn thuốc")
        title.setStyleSheet(f"font-size: {FONT_SIZE_XL}px; font-weight: 700; color: {PRIMARY_COLOR};")
        title.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(title)

        subtitle = QLabel("Quản lý các đơn thuốc của bạn tại đây")
        subtitle.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {HINT_COLOR};")
        subtitle.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(subtitle)

        top_row.addWidget(center_widget, stretch=1, alignment=Qt.AlignVCenter)

        self.bell_btn = QToolButton()
        self.bell_btn.setIcon(QIcon("assets/bell.png"))
        self.bell_btn.setIconSize(QSize(28, 28))
        self.bell_btn.setFixedSize(36, 36)
        self.bell_btn.setStyleSheet("background: transparent;")
        top_row.addWidget(self.bell_btn, alignment=Qt.AlignVCenter)

        header_layout.addLayout(top_row)
        inner_layout.addWidget(header)

        # Search bar with icon inside
        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        search_layout.setSpacing(0)
        search_layout.setAlignment(Qt.AlignCenter)  # Center the input horizontally

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên đơn thuốc")
        self.search_input.setFixedHeight(56)
        self.search_input.setFixedWidth(350)  # Make the input narrower
        self.search_input.setStyleSheet(f"""
            font-size: {FONT_SIZE_MD}px;
            padding: 10px 10px 10px 10px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            background: #fff;
        """)
        # Add magnify icon inside input, bigger size
        magnify_icon = QIcon("assets/search-analytics.png")
        action = QAction(magnify_icon, "", self.search_input)
        action.setIconText("search")
        self.search_input.addAction(action, QLineEdit.LeadingPosition)
        self.search_input.setStyleSheet(self.search_input.styleSheet() + "QLineEdit::leading-icon { width: 36px; height: 36px; }")

        search_layout.addWidget(self.search_input)
        inner_layout.addWidget(search_frame)

        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect(self.search_input)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(Qt.gray)
        self.search_input.setGraphicsEffect(shadow)

        search_layout.addWidget(self.search_input)
        inner_layout.addWidget(search_frame)

        # Section title
        section_title = QLabel("Tất cả")
        section_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: #002D40; margin-top: 16px; margin-bottom: 8px; font-family: {FONT_FAMILY}")
        section_title.setAlignment(Qt.AlignLeft)
        inner_layout.addWidget(section_title)

        # Scroll area for prescriptions
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
            border: none;
            background: transparent;
            }
            QScrollArea > QWidget {
            background: transparent;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
            background: transparent;
            }
        """)
        self.scroll_area.viewport().setStyleSheet("background: transparent;")
        self.prescriptions_container = QWidget()
        self.prescriptions_layout = QVBoxLayout(self.prescriptions_container)
        self.prescriptions_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # Center horizontally, top vertically
        self.prescriptions_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.prescriptions_container)
        inner_layout.addWidget(self.scroll_area)

        # --- Add a sample prescription card for preview ---
        sample_prescription = {
            "name": "Thuốc tuyến giáp",
            "category_name": "Mãn tính",
            "created_at": "2024-06-01",
            "hospital_name": "Bệnh viện Bạch Mai",
            "medicines": [
                {
                    "medicine_name": "Levothyroxine",
                    "type": "Viên nén",
                    "quantity_per_time": "1",
                    "usage_time": ["Sáng"],
                },
                {
                    "medicine_name": "Calcium",
                    "type": "Viên nén",
                    "quantity_per_time": "2",
                    "usage_time": ["Trưa", "Tối"],
                }
            ]
        }
        # Keep a reference to avoid garbage collection
        self._sample_card = PrescriptionCard(sample_prescription)
        self.prescriptions_layout.addWidget(self._sample_card)

        # Add button
        self.add_btn = QPushButton("Thêm đơn thuốc")
        self.add_btn.setStyleSheet("background: #406D96; color: white; font-size: 16px; border-radius: 8px; padding: 10px; margin-top: 16px; margin-bottom: 16px;")
        inner_layout.addWidget(self.add_btn)

        # Add the inner_widget to the outer_layout
        outer_layout.addWidget(inner_widget)
