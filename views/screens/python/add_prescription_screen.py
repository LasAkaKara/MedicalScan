from PySide6.QtCore import Signal
from views.screens.pyside.add_prescription_screen_ui import AddPrescriptionScreenUI
from services.database_service import DatabaseService

class AddPrescriptionScreen(AddPrescriptionScreenUI):
    go_to_prescription = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancel_btn.clicked.connect(self.handle_cancel)
        self.save_btn.clicked.connect(self.handle_save)
        self.db = DatabaseService()
        self.user_id = 2;
    
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

    def handle_cancel(self):
        self.go_to_prescription.emit()

    def handle_save(self):
        data = self.get_prescription_data()
        print("Prescription data:", data)
        result = self.db.add_prescription(
            user_id=self.user_id,
            name=data["name"],
            hospital_name=data["hospital_name"],
            category_name=data["category_name"],
            medicine_details=data["medicine_details"]
        )
        if result:
            print("Prescription added successfully!")
            self.go_to_prescription.emit()
        else:
            print("Failed to add prescription.")