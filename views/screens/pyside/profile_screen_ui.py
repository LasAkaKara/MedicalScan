# #:import utils kivy.utils
# #:import dp kivy.metrics.dp

# <PasswordChangeDialog>:
#     size_hint_y: None
#     height: "260dp"
    
#     BoxLayout:
#         orientation: "vertical"
#         spacing: "20dp"
#         size_hint_y: None
#         height: self.minimum_height
        
#         MDTextField:
#             id: current_password_field
#             hint_text: "Current Password"
#             password: True
#             helper_text: root.current_password_error
#             helper_text_mode: "on_error"
#             on_text: root.current_password = self.text
#             error: True if root.current_password_error else False
#             size_hint_y: None
#             height: self.minimum_height
        
#         MDTextField:
#             id: new_password_field
#             hint_text: "New Password"
#             password: True
#             helper_text: root.new_password_error
#             helper_text_mode: "on_error"
#             on_text: root.new_password = self.text
#             error: True if root.new_password_error else False
#             size_hint_y: None
#             height: self.minimum_height
        
#         MDTextField:
#             id: confirm_password_field
#             hint_text: "Confirm New Password"
#             password: True
#             helper_text: root.confirm_password_error
#             helper_text_mode: "on_error"
#             on_text: root.confirm_password = self.text
#             error: True if root.confirm_password_error else False
#             size_hint_y: None
#             height: self.minimum_height

# <EditProfileDialog>:
#     size_hint_y: None
#     height: "260dp"

#     BoxLayout:
#         orientation: "vertical"
#         size_hint_y: None
#         height: self.minimum_height
#         spacing: dp(16)
        
#         MDLabel:
#             text: "Edit Personal Information"
#             font_style: "H6"
#             size_hint_y: None
#             height: dp(40)
        
#         MDTextField:
#             id: email_field
#             hint_text: "Email"
#             text: root.email
#             size_hint_y: None
#             height: dp(48)
#             helper_text: "example@email.com"
#             helper_text_mode: "on_focus"
        
#         MDTextField:
#             id: full_name_field
#             hint_text: "Full Name"
#             text: root.full_name
#             size_hint_y: None
#             height: dp(48)
        
#         MDTextField:
#             id: phone_field
#             hint_text: "Phone"
#             text: root.phone
#             size_hint_y: None
#             height: dp(48)
#             helper_text: "10-15 digits, optionally with + prefix"
#             helper_text_mode: "on_focus"

# <HealthConditionDialog>:
#     size_hint_y: None
#     height: "120dp"
    
#     BoxLayout:
#         orientation: "vertical"
#         spacing: "10dp"
#         size_hint_y: None
#         height: self.minimum_height
        
#         MDTextField:
#             id: condition_field
#             hint_text: "Health Condition"
#             helper_text: root.condition_error
#             helper_text_mode: "on_error"
#             on_text: root.condition = self.text
#             error: True if root.condition_error else False
#             size_hint_y: None
#             height: self.minimum_height

# <NotificationSwitch@MDBoxLayout>:
#     orientation: 'horizontal'
#     size_hint_y: None
#     height: dp(50)
#     spacing: dp(10)
#     padding: [0, dp(5), 0, dp(5)]
    
#     icon: 'bell'
#     title: 'Notification Title'
#     subtitle: 'Notification Description'
#     active: False
#     callback: None
    
#     MDIcon:
#         icon: root.icon
#         size_hint: None, None
#         size: dp(24), dp(24)
#         pos_hint: {'center_y': 0.5}
#         theme_text_color: "Custom"
#         text_color: utils.get_color_from_hex('#406D96')
    
#     BoxLayout:
#         orientation: 'vertical'
#         spacing: dp(2)
        
#         MDLabel:
#             text: root.title
#             font_style: 'Subtitle1'
#             size_hint_y: None
#             height: dp(24)
        
#         MDLabel:
#             text: root.subtitle
#             font_style: 'Caption'
#             theme_text_color: "Secondary"
#             size_hint_y: None
#             height: dp(16)
    
#     MDSwitch:
#         active: root.active
#         pos_hint: {'center_y': 0.5}
#         on_active: root.callback(self.active) if root.callback else None

# <HealthStatCard@MDCard>:
#     orientation: 'vertical'
#     size_hint_y: None
#     height: dp(120)
#     padding: dp(16)
#     md_bg_color: 1, 1, 1, 1
#     radius: [10]
#     elevation: 1
    
#     icon: 'pill'
#     title: 'Stat Title'
#     value: '0'
#     color: '#2196F3'
    
#     AnchorLayout:
#         anchor_x: 'center'
#         size_hint_y: None
#         height: dp(40)
        
#         MDIcon:
#             icon: root.icon
#             size_hint: None, None
#             size: dp(36), dp(36)
#             theme_text_color: "Custom"
#             text_color: utils.get_color_from_hex(root.color)
    
#     BoxLayout:
#         orientation: 'vertical'
#         spacing: dp(4)
        
#         MDLabel:
#             text: root.value
#             halign: 'center'
#             font_style: 'H4'
#             theme_text_color: "Custom"
#             text_color: utils.get_color_from_hex(root.color)
#             bold: True
#             size_hint_y: None
#             height: dp(40)
        
#         MDLabel:
#             text: root.title
#             halign: 'center'
#             font_style: 'Subtitle1'
#             size_hint_y: None
#             height: dp(20)

# <HealthConditionChip@MDBoxLayout>:
#     orientation: 'horizontal'
#     size_hint: None, None
#     height: dp(32)
#     width: self.minimum_width
#     padding: [dp(8), 0, dp(4), 0]
#     spacing: dp(4)
#     md_bg_color: utils.get_color_from_hex('#E3F2FD')
#     radius: [16]
    
#     condition: 'Condition'
#     callback: None
    
#     MDLabel:
#         text: root.condition
#         size_hint: None, None
#         size: self.texture_size
#         pos_hint: {'center_y': 0.5}
#         font_style: 'Body2'
    
#     MDIconButton:
#         icon: 'close'
#         size_hint: None, None
#         size: dp(24), dp(24)
#         pos_hint: {'center_y': 0.5}
#         theme_text_color: "Custom"
#         text_color: utils.get_color_from_hex('#406D96')
#         on_release: root.callback() if root.callback else None

# <ProfileScreen>:
#     BoxLayout:
#         orientation: 'vertical'
        
#         # Header
#         Header:
        
#         # Profile content
#         ScrollView:
#             do_scroll_x: False
#             bar_width: 0
            
#             BoxLayout:
#                 orientation: 'vertical'
#                 size_hint_y: None
#                 height: self.minimum_height
#                 padding: dp(16)
#                 spacing: dp(16)
                
#                 # Enhanced Profile Avatar Section
#                 MDCard:
#                     orientation: 'vertical'
#                     padding: dp(20)
#                     size_hint_y: None
#                     height: dp(180)
#                     md_bg_color: 1, 1, 1, 1
#                     radius: [15]
#                     elevation: 2
                    
#                     BoxLayout:
#                         orientation: 'horizontal'
#                         height: dp(120)
#                         size_hint_y: 0.5
#                         spacing: dp(28)
                        
#                         BoxLayout:
#                             orientation: 'vertical'
#                             size_hint_x: 0.3
                            
#                             AsyncImage:
#                                 source: "assets/avatar_placeholder.png"
#                                 size_hint: None, None
#                                 size: dp(80), dp(80)
#                                 pos_hint: {'center_x': 0.5}
#                                 radius: [40,]
#                                 canvas.before:
#                                     Color:
#                                         rgba: utils.get_color_from_hex('#E3F2FD')
#                                     Ellipse:
#                                         pos: self.pos
#                                         size: self.size
#                         BoxLayout:
#                             orientation: 'vertical'
#                             size_hint_x: 0.7
                            
#                             MDLabel:
#                                 text: root.full_name if root.full_name else "User"
#                                 font_style: "H5"
#                                 bold: True
                            
#                             MDLabel:
#                                 text: root.email if root.email else "Not provided"
#                                 font_style: "Body2"
#                                 theme_text_color: "Secondary"
                        
                    
#                     BoxLayout:
#                         orientation: "horizontal"
#                         size_hint_y: 0.5
#                         spacing: dp(20)
#                         MDRaisedButton:
#                             text: "Edit profile"
#                             on_release: root.toggle_edit_mode()

#                         MDRaisedButton:
#                             text: "Change your password"
#                             on_release: root.change_password()
                
#                 # Health Stats Section
#                 MDCard:
#                     orientation: 'vertical'
#                     padding: dp(16)
#                     spacing: dp(12)
#                     size_hint_y: None
#                     height: self.minimum_height
#                     md_bg_color: 1, 1, 1, 1
#                     radius: [15]
#                     elevation: 2
                    
#                     MDLabel:
#                         text: "Health Activity"
#                         font_style: "H6"
#                         size_hint_y: None
#                         height: dp(40)
                    
#                     GridLayout:
#                         cols: 2
#                         spacing: dp(12)
#                         size_hint_y: None
#                         height: dp(120)
                        
#                         HealthStatCard:
#                             icon: 'pill'
#                             title: 'Prescriptions'
#                             value: str(root.prescription_count)
#                             color: '#406D96'
                        
#                         HealthStatCard:
#                             icon: 'text-recognition'
#                             title: 'Total Scans'
#                             value: str(root.scan_count)
#                             color: '#4CAF50'
                    
#                     MDCard:
#                         orientation: 'horizontal'
#                         size_hint_y: None
#                         height: dp(60)
#                         padding: dp(16)
#                         spacing: dp(16)
#                         radius: [10]
                        
#                         MDIcon:
#                             icon: 'calendar-clock'
#                             size_hint: None, None
#                             size: dp(28), dp(28)
#                             pos_hint: {'center_y': 0.5}
                        
#                         BoxLayout:
#                             orientation: 'vertical'
#                             spacing: dp(4)
                            
#                             MDLabel:
#                                 text: "Last Activity"
#                                 font_style: 'Body2'
#                                 theme_text_color: "Secondary"
#                                 size_hint_y: None
#                                 height: dp(16)
                            
#                             MDLabel:
#                                 text: root.last_activity
#                                 font_style: 'Subtitle1'
#                                 size_hint_y: None
#                                 height: dp(24)
                
#                 # Health Conditions Section
#                 MDCard:
#                     orientation: 'vertical'
#                     padding: dp(16)
#                     spacing: dp(12)
#                     size_hint_y: None
#                     height: self.minimum_height
#                     md_bg_color: 1, 1, 1, 1
#                     radius: [15]
#                     elevation: 2
                    
#                     BoxLayout:
#                         orientation: 'horizontal'
#                         size_hint_y: None
#                         height: dp(40)
                        
#                         MDLabel:
#                             text: "Health Conditions"
#                             font_style: "H6"
#                             size_hint_y: None
#                             height: dp(40)
                        
#                         Widget:
#                             size_hint_x: 1
                        
#                         MDFlatButton:
#                             text: "+ Add"
#                             theme_text_color: "Custom"
#                             text_color: utils.get_color_from_hex('#406D96')
#                             pos_hint: {'center_y': 0.5}
#                             on_release: root.add_health_condition()
                    
#                     MDBoxLayout:
#                         id: health_conditions_container
#                         orientation: 'horizontal'
#                         size_hint_y: None
#                         height: self.minimum_height if self.children else dp(50)
#                         spacing: dp(8)
#                         padding: [0, dp(10), 0, dp(10)]
#                         adaptive_height: True
#                         flex_wrap: 'wrap'
                
#                 # Notification Preferences
#                 MDCard:
#                     orientation: "vertical"
#                     size_hint_y: None
#                     height: self.minimum_height
#                     md_bg_color: 1, 1, 1, 1
#                     padding: [22, 0, 30, 0]
#                     radius: [15]
#                     elevation: 2
                    
#                     MDLabel:
#                         text: "Notification Preferences"
#                         font_style: "H6"
#                         size_hint_y: None
#                         height: dp(40)
                    
#                     NotificationSwitch:
#                         icon: 'pill'
#                         title: 'Medication Reminders'
#                         subtitle: 'Get notified about your medications'
#                         active: root.notify_medication
#                         callback: lambda x: root.toggle_notification('medication')
                    
#                     NotificationSwitch:
#                         icon: 'autorenew'
#                         title: 'Refill Reminders'
#                         subtitle: 'Get notified when prescriptions need refilling'
#                         active: root.notify_refills
#                         callback: lambda x: root.toggle_notification('refills')
                    
#                     NotificationSwitch:
#                         icon: 'calendar'
#                         title: 'Appointment Reminders'
#                         subtitle: 'Get notified about upcoming appointments'
#                         active: root.notify_appointments
#                         callback: lambda x: root.toggle_notification('appointments')
                
#                 # Logout button at the bottom
#                 MDRaisedButton:
#                     text: "Logout"
#                     pos_hint: {"center_x": 0.5}
#                     md_bg_color: utils.get_color_from_hex('#F44336')
#                     on_release: app.root.switch_screen("login")
                
#                 # Add some padding at the bottom
#                 Widget:
#                     size_hint_y: None
#                     height: dp(20) 

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QGridLayout, QSpacerItem, QSizePolicy, QCheckBox, QGraphicsDropShadowEffect, QDialog, QLineEdit, QToolButton, QApplication
)
from PySide6.QtGui import QPixmap, QFont, QColor, QIcon
from PySide6.QtCore import Qt, QSize
from themes import PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, HINT_COLOR, SECONDARY_TEXT, FONT_FAMILY

from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import QRectF, Qt, QSize

class OverlayModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.card = QWidget(self)
        layout.addWidget(self.card, alignment=Qt.AlignCenter)

    def showEvent(self, event):
        # Make the dialog cover the whole screen
        screen = self.screen() or QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            self.setGeometry(screen_geometry)
        super().showEvent(event)

    def paintEvent(self, event):
        # Draw a semi-transparent black overlay
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))  # 120 = ~50% opacity
        painter.end()


class EditProfileModal(OverlayModal):
    def __init__(self, name, email, phone, on_save, parent=None):
        super().__init__(parent)
        self.card.setFixedWidth(380)
        self.card.setStyleSheet("""
            background: #fff; border-radius: 18px; padding: 28px;
            border: 1px solid #e0e0e0;
        """)
        layout = QVBoxLayout(self.card)
        layout.setSpacing(18)

        title = QLabel("Chỉnh sửa thông tin")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2F3A56; padding: 0px; border: none;")
        layout.addWidget(title, alignment=Qt.AlignHCenter)

        # Label + Input for Tên
        name_label = QLabel("Tên")
        name_label.setStyleSheet(f"font-size: 14px; color: {TEXT_COLOR}; font-weight: 500; border: none; padding: 0px; margin: 0px; min-width: 0px; min-height: 0px;")
        layout.addWidget(name_label)
        self.name_edit = QLineEdit(name)
        self.name_edit.setPlaceholderText("Tên")
        self.name_edit.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #e0e0e0;")
        layout.addWidget(self.name_edit)

        # Label + Input for Email
        email_label = QLabel("Email")
        email_label.setStyleSheet(f"font-size: 14px; color: {TEXT_COLOR}; font-weight: 500; border: none; padding: 0px; margin: 0px; min-width: 0px; min-height: 0px;")
        layout.addWidget(email_label)
        self.email_edit = QLineEdit(email)
        self.email_edit.setPlaceholderText("Email")
        self.email_edit.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #e0e0e0;")
        layout.addWidget(self.email_edit)

        # Label + Input for Số điện thoại
        phone_label = QLabel("Số điện thoại")
        phone_label.setStyleSheet(f"font-size: 14px; color: {TEXT_COLOR}; font-weight: 500; border: none; padding: 0px; margin: 0px; min-width: 0px; min-height: 0px;")
        layout.addWidget(phone_label)
        self.phone_edit = QLineEdit(phone)
        self.phone_edit.setPlaceholderText("Số điện thoại")
        self.phone_edit.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #e0e0e0;")
        layout.addWidget(self.phone_edit)

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Lưu")
        save_btn.setStyleSheet("background: #2F3A56; color: white; border-radius: 8px; padding: 8px 18px;")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setStyleSheet("background: #e0e0e0; color: #2F3A56; border-radius: 8px; padding: 8px 18px;")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

        self.on_save = on_save

    def accept(self):
        if self.on_save:
            self.on_save(
                self.name_edit.text(),
                self.email_edit.text(),
                self.phone_edit.text()
            )
        super().accept()


class ChangePasswordModal(OverlayModal):
    def __init__(self, on_change, parent=None):
        super().__init__(parent)
        self.card.setFixedWidth(380)
        self.card.setStyleSheet("""
            background: #fff; border-radius: 18px; padding: 28px;
            border: 1px solid #e0e0e0;
        """)
        layout = QVBoxLayout(self.card)
        layout.setSpacing(18)

        title = QLabel("Đổi mật khẩu")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2F3A56; padding: 0px; border: none;")
        layout.addWidget(title, alignment=Qt.AlignHCenter)

        # Label + Input for Mật khẩu hiện tại
        current_label = QLabel("Mật khẩu hiện tại")
        current_label.setStyleSheet(f"font-size: 14px; color: {TEXT_COLOR}; font-weight: 500; border: none; padding: 0px; margin: 0px; min-width: 0px; min-height: 0px;")
        layout.addWidget(current_label)
        self.current_pw = self._password_field("Mật khẩu hiện tại")
        layout.addLayout(self.current_pw['layout'])

        # Label + Input for Mật khẩu mới
        new_label = QLabel("Mật khẩu mới")
        new_label.setStyleSheet(f"font-size: 14px; color: {TEXT_COLOR}; font-weight: 500; border: none; padding: 0px; margin: 0px; min-width: 0px; min-height: 0px;")
        layout.addWidget(new_label)
        self.new_pw = self._password_field("Mật khẩu mới")
        layout.addLayout(self.new_pw['layout'])

        # Label + Input for Xác nhận mật khẩu
        confirm_label = QLabel("Xác nhận mật khẩu")
        confirm_label.setStyleSheet(f"font-size: 14px; color: {TEXT_COLOR}; font-weight: 500; border: none; padding: 0px; margin: 0px; min-width: 0px; min-height: 0px;")
        layout.addWidget(confirm_label)
        self.confirm_pw = self._password_field("Xác nhận mật khẩu")
        layout.addLayout(self.confirm_pw['layout'])

        btn_row = QHBoxLayout()
        change_btn = QPushButton("Đổi mật khẩu")
        change_btn.setStyleSheet("background: #2F3A56; color: white; border-radius: 8px; padding: 8px 18px;")
        change_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setStyleSheet("background: #e0e0e0; color: #2F3A56; border-radius: 8px; padding: 8px 18px;")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(change_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

        self.on_change = on_change

    def _password_field(self, placeholder):
        layout = QHBoxLayout()
        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        edit.setEchoMode(QLineEdit.Password)
        edit.setStyleSheet("border-radius: 8px; padding: 8px;")
        show_btn = QToolButton()
        show_btn.setIcon(QIcon("assets/eye-close.png"))
        show_btn.setFixedSize(32, 32)
        show_btn.setCheckable(True)
        show_btn.setStyleSheet("background: transparent; border: none; padding: 0px; margin: 0px;min-width: 0px; min-height: 0px;")
        def toggle():
            edit.setEchoMode(QLineEdit.Normal if show_btn.isChecked() else QLineEdit.Password)
            show_btn.setIcon(QIcon("assets/eye-open.png") if show_btn.isChecked() else QIcon("assets/eye-close.png"))
        show_btn.clicked.connect(toggle)
        layout.addWidget(edit)
        layout.addWidget(show_btn)
        return {'layout': layout, 'edit': edit, 'show_btn': show_btn}

    def accept(self):
        if self.on_change:
            self.on_change(
                self.current_pw['edit'].text(),
                self.new_pw['edit'].text(),
                self.confirm_pw['edit'].text()
            )
        super().accept()

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

class ProfileScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # --- Header Section ---
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        # Back button
        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon("assets/back.png"))  # Use your back icon path
        self.back_btn.setIconSize(QSize(28, 28))
        self.back_btn.setFixedSize(48, 48)
        self.back_btn.setStyleSheet("""
            QPushButton {
            border: none;
            background: transparent;
            }
        """)
        header_layout.addWidget(self.back_btn, alignment=Qt.AlignVCenter)

        # Title and subtitle in a vertical layout
        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        title = QLabel("Hồ sơ")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {TEXT_COLOR}; font-family: {FONT_FAMILY};")
        subtitle = QLabel("Quản lý tài khoản của bạn tại đây")
        subtitle.setStyleSheet(f"font-size: 13px; color: #406D96; font-family: {FONT_FAMILY};")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        header_layout.addLayout(title_col)

        header_layout.addStretch()
        main_layout.addWidget(header_widget)

        # --- User Info Card ---
        # User Info Card
        user_card = QFrame()
        user_card.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 18px;
                border: 1px solid #e0e0e0;
            }
        """)
        user_shadow = QGraphicsDropShadowEffect(self)
        user_shadow.setBlurRadius(18)
        user_shadow.setOffset(0, 4)
        user_shadow.setColor(QColor(0, 0, 0, 40))
        user_card.setGraphicsEffect(user_shadow)
        user_card_layout = QVBoxLayout(user_card)
        user_card_layout.setSpacing(10)
        user_card_layout.setContentsMargins(18, 18, 18, 18)

        # Avatar, username, email
        avatar_row = QHBoxLayout()
        self.avatar_label = QLabel()
        self.avatar_label.setPixmap(QPixmap("assets/circle-user.png").scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.avatar_label.setFixedSize(72, 72)
        self.avatar_label.setStyleSheet("border-radius: 36px; background: #e3f2fd; border:none;")
        avatar_row.addWidget(self.avatar_label)

        info_col = QVBoxLayout()
        self.full_name_label = QLabel("User")
        self.full_name_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {TEXT_COLOR}; border:none;")
        info_col.addWidget(self.full_name_label)
        self.email_label = QLabel("Not provided")
        self.email_label.setStyleSheet(f"font-size: 14px; color: {HINT_COLOR}; border:none;")
        info_col.addWidget(self.email_label)
        avatar_row.addLayout(info_col)
        avatar_row.addStretch()
        user_card_layout.addLayout(avatar_row)

        # Buttons
        btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("Chỉnh sửa")
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background: #2F3A56; color: white; border-radius: 8px; padding: 8px 18px; font-weight: bold;
            }
            QPushButton:hover { background: #27496d; }
        """)
        self.change_pw_btn = QPushButton("Đổi mật khẩu")
        self.change_pw_btn.setStyleSheet("""
            QPushButton {
                background: #e3f2fd; color: #406D96; border-radius: 8px; padding: 8px 18px; font-weight: bold;
                border: 1px solid #406D96;
            }
            QPushButton:hover { background: #b3e5fc; }
        """)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.change_pw_btn)
        user_card_layout.addLayout(btn_row)
        main_layout.addWidget(user_card)

        # Stats Card
        stats_card = QFrame()
        stats_card.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-radius: 18px;
                border: 1px solid #e0e0e0;
                font-family: 'Roboto', sans-serif;
                font-weight: 600;
            }
        """)
        stats_shadow = QGraphicsDropShadowEffect(self)
        stats_shadow.setBlurRadius(18)
        stats_shadow.setOffset(0, 4)
        stats_shadow.setColor(QColor(0, 0, 0, 40))
        stats_card.setGraphicsEffect(stats_shadow)
        stats_layout = QHBoxLayout(stats_card)
        stats_layout.setContentsMargins(18, 18, 18, 18)

        # Đơn thuốc
        prescription_box = QVBoxLayout()
        presc_icon = QLabel()
        presc_icon.setPixmap(QPixmap("assets/medical-icon.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        presc_icon.setStyleSheet("border:none;")
        presc_icon.setAlignment(Qt.AlignCenter)
        prescription_box.addWidget(presc_icon)
        self.prescription_count_label = QLabel("0")
        self.prescription_count_label.setAlignment(Qt.AlignCenter)
        self.prescription_count_label.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {PRIMARY_COLOR}; border:none;")
        prescription_box.addWidget(self.prescription_count_label)
        stats_layout.addLayout(prescription_box)

        # Lượt quét
        scan_box = QVBoxLayout()
        scan_icon = QLabel()
        scan_icon.setPixmap(QPixmap("assets/qr-code-scan.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        scan_icon.setStyleSheet("border:none;")
        scan_icon.setAlignment(Qt.AlignCenter)
        scan_box.addWidget(scan_icon)
        self.scan_count_label = QLabel("0")
        self.scan_count_label.setAlignment(Qt.AlignCenter)
        self.scan_count_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #43a047; border:none;")
        scan_box.addWidget(self.scan_count_label)
        stats_layout.addLayout(scan_box)

        main_layout.addWidget(stats_card)

        # Notification Card
        notif_card = QFrame()
        notif_card.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 18px;
                border: 1px solid #e0e0e0;
            }
        """)
        notif_shadow = QGraphicsDropShadowEffect(self)
        notif_shadow.setBlurRadius(18)
        notif_shadow.setOffset(0, 4)
        notif_shadow.setColor(QColor(0, 0, 0, 40))
        notif_card.setGraphicsEffect(notif_shadow)
        notif_layout = QVBoxLayout(notif_card)
        notif_layout.setSpacing(12)
        notif_layout.setContentsMargins(18, 18, 18, 18)

        notif_title = QLabel("Thông báo")
        notif_title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {PRIMARY_COLOR}; border:none;")
        notif_layout.addWidget(notif_title)

        # Notification rows in a borderless container
        notif_inner = QWidget()
        notif_inner_layout = QVBoxLayout(notif_inner)
        notif_inner_layout.setSpacing(8)
        notif_inner_layout.setContentsMargins(0, 0, 0, 0)
        notif_inner.setStyleSheet("background: transparent; border: none;")

        # Medication reminder
        notif_row1 = QHBoxLayout()
        # Icon
        med_icon = QLabel()
        med_icon.setPixmap(QPixmap("assets/medicine.png").scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        med_icon.setFixedSize(32, 32)
        notif_row1.addWidget(med_icon)
        # Title and subtitle
        med_text_col = QVBoxLayout()
        med_title = QLabel("Nhắc thuốc")
        med_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #2F3A56;")
        med_subtitle = QLabel("Nhận thông báo về thuốc của bạn")
        med_subtitle.setStyleSheet("font-size: 12px; color: #406D96;")
        med_text_col.addWidget(med_title)
        med_text_col.addWidget(med_subtitle)
        notif_row1.addLayout(med_text_col)
        notif_row1.addStretch()
        self.notif_medication = QSwitch()
        notif_row1.addWidget(self.notif_medication)
        notif_inner_layout.addLayout(notif_row1)

        # Refill reminder
        notif_row2 = QHBoxLayout()
        refill_icon = QLabel()
        refill_icon.setPixmap(QPixmap("assets/medicine_refill.png").scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        refill_icon.setFixedSize(32, 32)
        notif_row2.addWidget(refill_icon)
        refill_text_col = QVBoxLayout()
        refill_title = QLabel("Nhắc tái đơn")
        refill_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #2F3A56;")
        refill_subtitle = QLabel("Thông báo khi cần tái đơn thuốc")
        refill_subtitle.setStyleSheet("font-size: 12px; color: #406D96;")
        refill_text_col.addWidget(refill_title)
        refill_text_col.addWidget(refill_subtitle)
        notif_row2.addLayout(refill_text_col)
        notif_row2.addStretch()
        self.notif_refills = QSwitch()
        notif_row2.addWidget(self.notif_refills)
        notif_inner_layout.addLayout(notif_row2)

        notif_layout.addWidget(notif_inner)

        main_layout.addWidget(notif_card)

        # --- Logout Button ---
        main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.logout_btn = QPushButton("Đăng xuất")
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background: #F44336;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover { background: #d32f2f; }
        """)
        main_layout.addWidget(self.logout_btn)