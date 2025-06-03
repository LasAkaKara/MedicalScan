from PySide6.QtCore import Signal
from views.screens.pyside.add_prescription_screen_ui import AddPrescriptionScreenUI

class AddPrescriptionScreen(AddPrescriptionScreenUI):
    go_to_prescription = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancel_btn.clicked.connect(self.handle_cancel)
        self.save_btn.clicked.connect(self.handle_save)
    
    def get_prescription_data(self):
        return {
            "name": self.name_input.text(),
            "hospital_name": self.hospital_input.text(),
            "category_name": self.category_input.currentText(),
            "medicines": [form.get_data() for form in self.medicine_forms]
        }

    def handle_cancel(self):
        self.go_to_prescription.emit()

    def handle_save(self):
        data = self.get_prescription_data()
        print("Prescription data:", data)  # Print to terminal for debugging
        # TODO: Save to database here
        self.go_to_prescription.emit()