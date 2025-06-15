from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, 
    QComboBox, QScrollArea, QFrame, QCheckBox, QTextEdit, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QPixmap, QFont
from themes import PRIMARY_COLOR, TEXT_COLOR, FONT_FAMILY

class MedicineEditCard(QFrame):
    """Editable medicine card for confirmation screen"""
    
    def __init__(self, medicine_data, parent=None):
        super().__init__(parent)
        self.medicine_data = medicine_data
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background: #ffffff;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                margin-bottom: 8px;
                font-family: {FONT_FAMILY};
            }}
        """)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Medicine name (full width)
        name_layout = QHBoxLayout()
        name_label = QLabel("Tên thuốc:")
        name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151; min-width: 80px;")
        self.name_input = QLineEdit(self.medicine_data.get('medicine_name', ''))
        self.name_input.setStyleSheet(self.get_input_style())
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input, 1)
        layout.addLayout(name_layout)
        
        # Type and strength (side by side)
        type_strength_layout = QHBoxLayout()
        
        # Type
        type_label = QLabel("Loại:")
        type_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151; min-width: 50px;")
        self.type_input = QLineEdit(self.medicine_data.get('type', 'Viên'))
        self.type_input.setStyleSheet(self.get_input_style())
        
        # Strength
        strength_label = QLabel("Hàm lượng:")
        strength_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151; min-width: 80px;")
        self.strength_input = QLineEdit(self.medicine_data.get('strength', ''))
        self.strength_input.setStyleSheet(self.get_input_style())
        
        type_strength_layout.addWidget(type_label)
        type_strength_layout.addWidget(self.type_input, 1)
        type_strength_layout.addWidget(strength_label)
        type_strength_layout.addWidget(self.strength_input, 1)
        layout.addLayout(type_strength_layout)
        
        # Quantity and duration (side by side)
        qty_duration_layout = QHBoxLayout()
        
        # Quantity per time
        qty_label = QLabel("Liều dùng:")
        qty_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151; min-width: 70px;")
        self.qty_input = QLineEdit(self.medicine_data.get('quantity_per_time', ''))
        self.qty_input.setStyleSheet(self.get_input_style())
        
        # Duration
        duration_label = QLabel("Số ngày:")
        duration_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151; min-width: 60px;")
        self.duration_input = QLineEdit(self.medicine_data.get('duration_days', ''))
        self.duration_input.setStyleSheet(self.get_input_style())
        
        qty_duration_layout.addWidget(qty_label)
        qty_duration_layout.addWidget(self.qty_input, 1)
        qty_duration_layout.addWidget(duration_label)
        qty_duration_layout.addWidget(self.duration_input, 1)
        layout.addLayout(qty_duration_layout)
        
        # Usage times (horizontal layout)
        usage_layout = QHBoxLayout()
        usage_label = QLabel("Thời điểm:")
        usage_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151; min-width: 70px;")
        
        self.morning_cb = QCheckBox("Sáng")
        self.noon_cb = QCheckBox("Trưa")
        self.evening_cb = QCheckBox("Tối")
        
        # Set initial values
        usage_times = self.medicine_data.get('usage_time', [])
        for usage in usage_times:
            if isinstance(usage, dict):
                time_label = usage.get('time', '')
                if time_label == 'Sáng':
                    self.morning_cb.setChecked(True)
                elif time_label == 'Trưa':
                    self.noon_cb.setChecked(True)
                elif time_label == 'Tối':
                    self.evening_cb.setChecked(True)
        
        for cb in [self.morning_cb, self.noon_cb, self.evening_cb]:
            cb.setStyleSheet("font-size: 14px; color: #374151;")
        
        usage_layout.addWidget(usage_label)
        usage_layout.addWidget(self.morning_cb)
        usage_layout.addWidget(self.noon_cb)
        usage_layout.addWidget(self.evening_cb)
        usage_layout.addStretch()
        layout.addLayout(usage_layout)
        
        # Usage instruction (full width, smaller height)
        instruction_label = QLabel("Hướng dẫn sử dụng:")
        instruction_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151;")
        self.instruction_input = QTextEdit()
        self.instruction_input.setPlainText(self.medicine_data.get('usage_instruction', ''))
        self.instruction_input.setMaximumHeight(60)
        self.instruction_input.setStyleSheet(self.get_input_style())
        
        layout.addWidget(instruction_label)
        layout.addWidget(self.instruction_input)
    
    def get_input_style(self):
        """Get consistent input styling"""
        return """
            QLineEdit, QTextEdit {
                font-size: 14px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px;
                background: #f9fafb;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #3b82f6;
                background: white;
            }
        """
    
    def get_medicine_data(self):
        """Get the current medicine data from the form"""
        usage_times = []
        if self.morning_cb.isChecked():
            usage_times.append({"time": "Sáng", "quantity": 1})
        if self.noon_cb.isChecked():
            usage_times.append({"time": "Trưa", "quantity": 1})
        if self.evening_cb.isChecked():
            usage_times.append({"time": "Tối", "quantity": 1})
        
        return {
            "medicine_name": self.name_input.text().strip(),
            "type": self.type_input.text().strip(),
            "strength": self.strength_input.text().strip(),
            "quantity_per_time": self.qty_input.text().strip(),
            "duration_days": self.duration_input.text().strip(),
            "usage_instruction": self.instruction_input.toPlainText().strip(),
            "usage_time": usage_times,
            "total_quantity": ""  # Can be calculated if needed
        }

class PrescriptionConfirmScreenUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xác nhận đơn thuốc")
        self.medicine_cards = []
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header (fixed at top)
        header_widget = QWidget()
        header_widget.setStyleSheet("background: white; border-bottom: 1px solid #e5e7eb;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(16, 16, 16, 16)
        header_layout.setSpacing(12)
        
        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon("assets/back.png"))
        self.back_btn.setIconSize(QSize(24, 24))
        self.back_btn.setFixedSize(40, 40)
        self.back_btn.setStyleSheet("background: transparent; border: none;")
        
        title_label = QLabel("Xác nhận thông tin đơn thuốc")
        title_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {TEXT_COLOR}; font-family: {FONT_FAMILY};")
        
        header_layout.addWidget(self.back_btn)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addWidget(header_widget)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background: #f8fafc; 
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9ca3af;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Content widget
        content_widget = QWidget()
        content_widget.setStyleSheet("background: #f8fafc;")
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(16)
        
        # Warning message
        self.create_warning_section()
        
        # Basic information section
        self.create_basic_info_section()
        
        # Medicines section
        self.create_medicines_section()
        
        # Add stretch to push content to top
        self.content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Bottom buttons (fixed at bottom)
        self.create_bottom_buttons(main_layout)
    
    def create_warning_section(self):
        """Create warning message section"""
        warning_frame = QFrame()
        warning_frame.setStyleSheet("""
            QFrame {
                background: #fef3c7;
                border: 1px solid #f59e0b;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        warning_layout = QHBoxLayout(warning_frame)
        warning_layout.setContentsMargins(12, 12, 12, 12)
        warning_layout.setSpacing(8)
        
        warning_icon = QLabel("⚠️")
        warning_icon.setStyleSheet("font-size: 16px;")
        warning_text = QLabel("Vui lòng kiểm tra và chỉnh sửa thông tin nếu cần thiết. Dữ liệu được trích xuất tự động có thể chưa chính xác hoàn toàn.")
        warning_text.setWordWrap(True)
        warning_text.setStyleSheet("font-size: 14px; color: #92400e; font-weight: 500;")
        
        warning_layout.addWidget(warning_icon)
        warning_layout.addWidget(warning_text, 1)
        
        self.content_layout.addWidget(warning_frame)
    
    def create_basic_info_section(self):
        """Create the basic prescription information section"""
        basic_info_frame = QFrame()
        basic_info_frame.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
        """)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect(basic_info_frame)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        shadow.setColor(Qt.gray)
        basic_info_frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(basic_info_frame)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Section title
        title = QLabel("Thông tin bệnh nhân")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {PRIMARY_COLOR}; margin-bottom: 8px;")
        layout.addWidget(title)
        
        # Grid layout for form fields (2 columns)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(3, 1)
        
        # Row 1: Patient name and Doctor name
        grid_layout.addWidget(self.create_field_label("Tên bệnh nhân:"), 0, 0)
        self.patient_name_input = QLineEdit()
        self.patient_name_input.setStyleSheet(self.get_input_style())
        grid_layout.addWidget(self.patient_name_input, 0, 1)
        
        grid_layout.addWidget(self.create_field_label("Bác sĩ:"), 0, 2)
        self.doctor_name_input = QLineEdit()
        self.doctor_name_input.setStyleSheet(self.get_input_style())
        grid_layout.addWidget(self.doctor_name_input, 0, 3)
        
        # Row 2: Age and Weight
        grid_layout.addWidget(self.create_field_label("Tuổi:"), 1, 0)
        self.age_input = QLineEdit()
        self.age_input.setStyleSheet(self.get_input_style())
        grid_layout.addWidget(self.age_input, 1, 1)
        
        grid_layout.addWidget(self.create_field_label("Cân nặng:"), 1, 2)
        self.weight_input = QLineEdit()
        self.weight_input.setStyleSheet(self.get_input_style())
        grid_layout.addWidget(self.weight_input, 1, 3)
        
        # Row 3: Gender and Hospital
        grid_layout.addWidget(self.create_field_label("Giới tính:"), 2, 0)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "Nam", "Nữ"])
        self.gender_combo.setStyleSheet(self.get_input_style())
        grid_layout.addWidget(self.gender_combo, 2, 1)
        
        grid_layout.addWidget(self.create_field_label("Bệnh viện:"), 2, 2)
        self.hospital_input = QLineEdit()
        self.hospital_input.setStyleSheet(self.get_input_style())
        grid_layout.addWidget(self.hospital_input, 2, 3)
        
        layout.addLayout(grid_layout)
        
        # Diagnosis (full width)
        diagnosis_label = self.create_field_label("Chẩn đoán:")
        self.diagnosis_input = QTextEdit()
        self.diagnosis_input.setMaximumHeight(80)
        self.diagnosis_input.setStyleSheet(self.get_input_style())
        
        layout.addWidget(diagnosis_label)
        layout.addWidget(self.diagnosis_input)
        
        self.content_layout.addWidget(basic_info_frame)
    
    def create_medicines_section(self):
        """Create the medicines section"""
        medicines_frame = QFrame()
        medicines_frame.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
        """)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect(medicines_frame)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        shadow.setColor(Qt.gray)
        medicines_frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(medicines_frame)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Section title with add button
        title_layout = QHBoxLayout()
        title = QLabel("Danh sách thuốc")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {PRIMARY_COLOR};")
        
        self.add_medicine_btn = QPushButton("+ Thêm thuốc")
        self.add_medicine_btn.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: #2563eb;
            }}
        """)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(self.add_medicine_btn)
        layout.addLayout(title_layout)
        
        # Medicines container
        self.medicines_container = QWidget()
        self.medicines_layout = QVBoxLayout(self.medicines_container)
        self.medicines_layout.setSpacing(8)
        self.medicines_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.medicines_container)
        
        self.content_layout.addWidget(medicines_frame)
    
    def create_bottom_buttons(self, main_layout):
        """Create bottom action buttons"""
        button_widget = QWidget()
        button_widget.setStyleSheet("background: white; border-top: 1px solid #e5e7eb;")
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(16, 16, 16, 16)
        button_layout.setSpacing(12)
        
        self.cancel_btn = QPushButton("Hủy")
        self.cancel_btn.setFixedHeight(44)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e5e7eb;
            }
        """)
        
        self.save_btn = QPushButton("Lưu đơn thuốc")
        self.save_btn.setFixedHeight(44)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0px 24px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: #2563eb;
            }}
        """)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        
        main_layout.addWidget(button_widget)
    
    def create_field_label(self, text):
        """Create a styled field label"""
        label = QLabel(text)
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151;")
        return label
    
    def get_input_style(self):
        """Get consistent input styling"""
        return """
            QLineEdit, QComboBox, QTextEdit {
                font-size: 14px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px;
                background: #f9fafb;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border-color: #3b82f6;
                background: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(assets/down-arrow.png);
                width: 12px;
                height: 12px;
            }
        """
    
    def set_prescription_data(self, prescription_data):
        """Set the prescription data in the form"""
        # Set basic information
        self.patient_name_input.setText(prescription_data.get('patient_name', ''))
        self.doctor_name_input.setText(prescription_data.get('doctor_name', ''))
        self.age_input.setText(str(prescription_data.get('age', '')))
        self.weight_input.setText(str(prescription_data.get('weight', '')))
        self.hospital_input.setText(prescription_data.get('hospital_name', ''))
        self.diagnosis_input.setPlainText(prescription_data.get('diagnosis', ''))
        
        # Set gender
        gender = prescription_data.get('gender', '')
        if gender in ['Nam', 'Nữ']:
            self.gender_combo.setCurrentText(gender)
        
        # Clear existing medicine cards
        self.clear_medicine_cards()
        
        # Add medicine cards
        medicines = prescription_data.get('medicines', [])
        for medicine in medicines:
            self.add_medicine_card(medicine)
        
        # If no medicines, add one empty card
        if not medicines:
            self.add_medicine_card({})
    
    def add_medicine_card(self, medicine_data=None):
        """Add a new medicine card"""
        if medicine_data is None:
            medicine_data = {}
        
        card = MedicineEditCard(medicine_data)
        self.medicine_cards.append(card)
        self.medicines_layout.addWidget(card)
    
    def clear_medicine_cards(self):
        """Clear all medicine cards"""
        for card in self.medicine_cards:
            card.setParent(None)
        self.medicine_cards.clear()
    
    def get_prescription_data(self):
        """Get the current prescription data from the form"""
        medicines = []
        for card in self.medicine_cards:
            medicine_data = card.get_medicine_data()
            if medicine_data['medicine_name']:  # Only include if medicine name is provided
                medicines.append(medicine_data)
        
        return {
            'patient_name': self.patient_name_input.text().strip(),
            'doctor_name': self.doctor_name_input.text().strip(),
            'age': self.age_input.text().strip(),
            'weight': self.weight_input.text().strip(),
            'gender': self.gender_combo.currentText(),
            'hospital_name': self.hospital_input.text().strip(),
            'diagnosis': self.diagnosis_input.toPlainText().strip(),
            'prescription_date': '',
            'medicines': medicines
        }