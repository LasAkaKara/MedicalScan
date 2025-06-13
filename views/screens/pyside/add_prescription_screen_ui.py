from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QDateEdit, QFrame, QSpinBox, QCheckBox, QSizePolicy, QGraphicsDropShadowEffect, QToolButton, QScrollArea, QScroller
)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QIcon
from themes import FONT_SIZE_MD, FONT_SIZE_LG, TEXT_COLOR, HINT_COLOR, PRIMARY_COLOR

class MedicineForm(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 14px;
                border: 1px solid #e0e0e0;
                margin-bottom: 8px;
            }
        """)
        self.setFixedWidth(360)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 3)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(16, 12, 16, 12)

        # Name label and input
        name_label = QLabel("Tên thuốc")
        name_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #406D96; margin-bottom: 2px; border: none;")
        main_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên thuốc")
        self.name_input.setMinimumWidth(120)
        self.name_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px; border-radius: 8px; padding: 6px;
                border: 1px solid #bfc9d1;
                background: #fafdff;
            }
            QLineEdit:focus {
                border: 1.5px solid #406D96;
            }
        """)
        main_layout.addWidget(self.name_input)

        # Type
        type_label = QLabel("Loại thuốc")
        type_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #406D96; margin-bottom: 2px; border: none;")
        main_layout.addWidget(type_label)
        self.type_input = QComboBox()
        self.type_input.addItems(["Viên", "Ống", "Gói", "Khác"])
        self.type_input.setStyleSheet("""
            QComboBox {
            font-size: 15px; border-radius: 8px; padding: 6px 32px 6px 8px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QComboBox:focus {
            border: 1.5px solid #406D96;
            }
            QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 24px;
            border: none;
            }
            QComboBox::down-arrow {
            image: url(assets/down-arrow.png);
            width: 16px;
            height: 16px;
            margin-right: 4px;
            }
        """)
        main_layout.addWidget(self.type_input)

        # Strength
        strength_label = QLabel("Hàm lượng")
        strength_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #406D96; margin-bottom: 2px; border: none;")
        main_layout.addWidget(strength_label)
        self.strength_input = QLineEdit()
        self.strength_input.setPlaceholderText("Nhập hàm lượng")
        self.strength_input.setMinimumWidth(80)
        self.strength_input.setStyleSheet("""
            QLineEdit {
            font-size: 15px; border-radius: 8px; padding: 6px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QLineEdit:focus {
            border: 1.5px solid #406D96;
            }
        """)
        main_layout.addWidget(self.strength_input)

        # Total quantity label and input (NEW FIELD)
        total_qty_label = QLabel("Tổng số lượng thuốc")
        total_qty_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #406D96; margin-bottom: 2px; border: none;")
        main_layout.addWidget(total_qty_label)
        self.total_qty_input = QLineEdit()
        self.total_qty_input.setPlaceholderText("Nhập tổng số lượng thuốc")
        self.total_qty_input.setMinimumWidth(80)
        self.total_qty_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px; border-radius: 8px; padding: 6px;
                border: 1px solid #bfc9d1;
                background: #fafdff;
            }
            QLineEdit:focus {
                border: 1.5px solid #406D96;
            }
        """)
        main_layout.addWidget(self.total_qty_input)

        # Quantity label and input
        qty_label = QLabel("Số lượng mỗi lần")
        qty_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #406D96; margin-bottom: 2px; border: none;")
        main_layout.addWidget(qty_label)
        self.qty_input = QLineEdit()
        self.qty_input.setPlaceholderText("Nhập số lượng")
        self.qty_input.setMinimumWidth(80)
        self.qty_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px; border-radius: 8px; padding: 6px;
                border: 1px solid #bfc9d1;
                background: #fafdff;
            }
            QLineEdit:focus {
                border: 1.5px solid #406D96;
            }
        """)
        main_layout.addWidget(self.qty_input)

        # Usage time label and checkboxes
        usage_time_label = QLabel("Thời điểm dùng")
        usage_time_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #406D96; margin-bottom: 2px; border: none;")
        main_layout.addWidget(usage_time_label)
        row2 = QHBoxLayout()
        self.morning_cb = QCheckBox("Sáng")
        self.afternoon_cb = QCheckBox("Trưa")
        self.evening_cb = QCheckBox("Tối")
        for cb in [self.morning_cb, self.afternoon_cb, self.evening_cb]:
            cb.setStyleSheet("font-size: 14px;")
            row2.addWidget(cb)
        row2.addStretch()
        main_layout.addLayout(row2)

        # Duration days label and input
        duration_label = QLabel("Số ngày dùng")
        duration_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #406D96; margin-bottom: 2px; border: none;")
        main_layout.addWidget(duration_label)
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Nhập số ngày dùng")
        self.duration_input.setMinimumWidth(80)
        self.duration_input.setStyleSheet("""
            QLineEdit {
            font-size: 15px; border-radius: 8px; padding: 6px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QLineEdit:focus {
            border: 1.5px solid #406D96;
            }
        """)
        main_layout.addWidget(self.duration_input)

        # Usage instruction label and input
        usage_label = QLabel("Hướng dẫn (tùy chọn)")
        usage_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #406D96; margin-bottom: 2px; border: none;")
        main_layout.addWidget(usage_label)
        row3 = QHBoxLayout()
        self.usage_input = QLineEdit()
        self.usage_input.setPlaceholderText("Nhập hướng dẫn")
        self.usage_input.setMinimumWidth(120)
        self.usage_input.setStyleSheet("""
            QLineEdit {
            font-size: 15px; border-radius: 8px; padding: 6px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QLineEdit:focus {
            border: 1.5px solid #406D96;
            }
        """)
        row3.addWidget(self.usage_input)

        row3.addStretch()
        self.remove_btn = QPushButton(QIcon("assets/close.png"), "")
        self.remove_btn.setFixedSize(32, 32)
        self.remove_btn.setStyleSheet("""
            QPushButton {
            background: #f8d7da;
            border-radius: 16px;
            }
            QPushButton:hover {
            background: #f5c2c7;
            }
        """)
        row3.addWidget(self.remove_btn)
        main_layout.addLayout(row3)

    def get_data(self):
        usage_time = []
        if self.morning_cb.isChecked():
            usage_time.append("Sáng")
        if self.afternoon_cb.isChecked():
            usage_time.append("Trưa")
        if self.evening_cb.isChecked():
            usage_time.append("Tối")
        return {
            "medicine_name": self.name_input.text(),
            "type": self.type_input.currentText(),
            "strength": self.strength_input.text(),
            "total_quantity": self.total_qty_input.text(),
            "quantity_per_time": self.qty_input.text(),
            "duration_days": self.duration_input.text(),
            "usage_instruction": self.usage_input.text(),
            "usage_time": usage_time  # Now just a list of checked times
        }

class AddPrescriptionScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm đơn thuốc mới")
        self.setStyleSheet("background: #F8FAFC;")
        
        # --- Main scroll area ---
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide vertical scrollbar
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)

        # --- Content widget inside scroll area ---
        content = QWidget()
        scroll.setWidget(content)
        main_layout = QVBoxLayout(content)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(18)

        # Title
        title = QLabel("Thêm đơn thuốc mới")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #406D96; margin-bottom: 8px;")
        main_layout.addWidget(title)

        # Prescription info fields
        form = QFrame()
        form.setStyleSheet("""
            QFrame {
                background: #fff;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
                font-family: 'Roboto', sans-serif;
            }
        """)
        form_shadow = QGraphicsDropShadowEffect(form)
        form_shadow.setBlurRadius(12)
        form_shadow.setOffset(0, 3)
        form_shadow.setColor(Qt.gray)
        form.setGraphicsEffect(form_shadow)

        form_layout = QVBoxLayout(form)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(20, 16, 20, 16)

        # Name input
        name_label = QLabel("Tên đơn thuốc")
        name_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên đơn thuốc")
        self.name_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px; border-radius: 8px; padding: 8px;
                border: 1px solid #bfc9d1;
                background: #fafdff;
            }
            QLineEdit:focus {
                border: 1.5px solid #406D96;
            }
        """)
        form_layout.addWidget(self.name_input)

        # Patient name
        patient_label = QLabel("Họ tên bệnh nhân")
        patient_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(patient_label)
        self.patient_input = QLineEdit()
        self.patient_input.setPlaceholderText("Nhập họ tên bệnh nhân")
        self.patient_input.setStyleSheet("""
            QLineEdit {
            font-size: 15px; border-radius: 8px; padding: 8px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QLineEdit:focus {
            border: 1.5px solid #406D96;
            }
        """)
        form_layout.addWidget(self.patient_input)

        # Doctor name
        doctor_label = QLabel("Bác sĩ")
        doctor_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(doctor_label)
        self.doctor_input = QLineEdit()
        self.doctor_input.setPlaceholderText("Nhập tên bác sĩ")
        self.doctor_input.setStyleSheet("""
            QLineEdit {
            font-size: 15px; border-radius: 8px; padding: 8px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QLineEdit:focus {
            border: 1.5px solid #406D96;
            }
        """)
        form_layout.addWidget(self.doctor_input)

        # Age
        age_label = QLabel("Tuổi")
        age_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(age_label)
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Nhập tuổi")
        self.age_input.setStyleSheet("""
            QLineEdit {
            font-size: 15px; border-radius: 8px; padding: 8px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QLineEdit:focus {
            border: 1.5px solid #406D96;
            }
        """)
        form_layout.addWidget(self.age_input)

        # Weight
        weight_label = QLabel("Cân nặng")
        weight_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(weight_label)
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Nhập cân nặng (ví dụ: 58kg)")
        self.weight_input.setStyleSheet("""
            QLineEdit {
            font-size: 15px; border-radius: 8px; padding: 8px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QLineEdit:focus {
            border: 1.5px solid #406D96;
            }
        """)
        form_layout.addWidget(self.weight_input)

        # Gender
        gender_label = QLabel("Giới tính")
        gender_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(gender_label)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Nam", "Nữ", "Khác"])
        self.gender_input.setStyleSheet("""
            QComboBox {
            font-size: 15px; border-radius: 8px; padding: 8px 36px 8px 8px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QComboBox:focus {
            border: 1.5px solid #406D96;
            }
            QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 28px;
            border: none;
            }
            QComboBox::down-arrow {
            image: url(assets/down-arrow.png);
            width: 20px;
            height: 20px;
            margin-right: 6px;
            }
        """)
        form_layout.addWidget(self.gender_input)

        # Diagnosis
        diagnosis_label = QLabel("Chẩn đoán")
        diagnosis_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(diagnosis_label)
        self.diagnosis_input = QLineEdit()
        self.diagnosis_input.setPlaceholderText("Nhập chẩn đoán")
        self.diagnosis_input.setStyleSheet("""
            QLineEdit {
            font-size: 15px; border-radius: 8px; padding: 8px;
            border: 1px solid #bfc9d1;
            background: #fafdff;
            }
            QLineEdit:focus {
            border: 1.5px solid #406D96;
            }
        """)
        form_layout.addWidget(self.diagnosis_input)

        # Hospital input
        hospital_label = QLabel("Bệnh viện")
        hospital_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(hospital_label)
        self.hospital_input = QLineEdit()
        self.hospital_input.setPlaceholderText("Nhập tên bệnh viện")
        self.hospital_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px; border-radius: 8px; padding: 8px;
                border: 1px solid #bfc9d1;
                background: #fafdff;
            }
            QLineEdit:focus {
                border: 1.5px solid #406D96;
            }
        """)
        form_layout.addWidget(self.hospital_input)

        # Category input
        category_label = QLabel("Loại đơn thuốc")
        category_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_COLOR}; margin-bottom: 2px; border: none;")
        form_layout.addWidget(category_label)
        self.category_input = QComboBox()
        self.category_input.addItems(["Bệnh mãn tính", "Điều trị cấp tính", "Thực phẩm chức năng", "Khác"])
        self.category_input.setStyleSheet("""
            QComboBox {
                font-size: 15px; border-radius: 8px; padding: 8px 36px 8px 8px;
                border: 1px solid #bfc9d1;
                background: #fafdff;
            }
            QComboBox:focus {
                border: 1.5px solid #406D96;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border: none;
            }
            QComboBox::down-arrow {
                image: url(assets/down-arrow.png);
                width: 20px;
                height: 20px;
                margin-right: 6px;
            }
        """)
        form_layout.addWidget(self.category_input)

        main_layout.addWidget(form)

        # Medicines section
        med_section_title = QLabel("Danh sách thuốc")
        med_section_title.setStyleSheet("font-size: 17px; font-weight: bold; color: #002D40; margin-top: 8px;")
        main_layout.addWidget(med_section_title)

        self.meds_widget = QWidget()
        self.meds_layout = QVBoxLayout(self.meds_widget)
        self.meds_layout.setSpacing(20)
        self.meds_layout.setContentsMargins(0, 0, 0, 0)
        self.meds_layout.setAlignment(Qt.AlignHCenter)
        main_layout.addWidget(self.meds_widget)

        # Add medicine button
        self.add_med_btn = QPushButton(QIcon("assets/plus.png"), "Thêm thuốc")
        self.add_med_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background: #e3eaf6;
                border-radius: 20px;
                padding: 8px 20px;
                color: #406D96;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #d0e2f2;
            }
        """)
        self.add_med_btn.setFixedHeight(40)
        main_layout.addWidget(self.add_med_btn, alignment=Qt.AlignLeft)

        # Bottom buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.save_btn = QPushButton("Lưu")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #406D96;
                color: white;
                font-weight: bold;
                border-radius: 12px;
                padding: 10px 32px;
            }
            QPushButton:hover {
                background: #27496d;
            }
        """)
        save_shadow = QGraphicsDropShadowEffect(self.save_btn)
        save_shadow.setBlurRadius(12)
        save_shadow.setOffset(0, 3)
        save_shadow.setColor(Qt.gray)
        self.save_btn.setGraphicsEffect(save_shadow)
        btn_row.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Hủy")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: #e3eaf6;
                color: #406D96;
                font-weight: bold;
                border-radius: 12px;
                padding: 10px 32px;
            }
            QPushButton:hover {
                background: #d0e2f2;
            }
        """)
        btn_row.addWidget(self.cancel_btn)
        main_layout.addLayout(btn_row)

        # --- Logic for dynamic medicine forms ---
        self.medicine_forms = []
        self.add_medicine_form()
        self.add_med_btn.clicked.connect(self.add_medicine_form)

    def add_medicine_form(self):
        med_form = MedicineForm()
        self.meds_layout.addWidget(med_form)
        self.medicine_forms.append(med_form)
        med_form.remove_btn.clicked.connect(lambda: self.remove_medicine_form(med_form))

    def remove_medicine_form(self, med_form):
        self.meds_layout.removeWidget(med_form)
        med_form.setParent(None)
        self.medicine_forms.remove(med_form)

    def get_prescription_data(self):
        return {
            "name": self.name_input.text(),
            "hospital_name": self.hospital_input.text(),
            "category_name": self.category_input.currentText(),
            "medicine_details": {
                "patient_name": self.patient_input.text(),
                "doctor_name": self.doctor_input.text(),
                "age": self.age_input.text(),
                "weight": self.weight_input.text(),
                "gender": self.gender_input.currentText(),
                "diagnosis": self.diagnosis_input.text(),
                "medicines": [form.get_data() for form in self.medicine_forms]
            }
        }