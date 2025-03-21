from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivymd.uix.card import MDCard
from services.database_service import DatabaseService
import json
from datetime import datetime

Builder.load_file('views/screens/kv/prescription_detail_screen.kv')

class MedicineDetailCard(MDCard):
    medicine_name = StringProperty("")
    usage_time = StringProperty("")
    quantity_per_time = StringProperty("")
    total_quantity = StringProperty("")
    usage_instruction = StringProperty("")
    duration_days = StringProperty("")
    medicine_info = StringProperty("")

class PrescriptionDetailScreen(Screen):
    prescription_id = NumericProperty(None)
    
    def on_enter(self):
        if self.prescription_id:
            self.load_prescription_details()
    
    def load_prescription_details(self):
        db = DatabaseService()
        prescription = db.get_prescription_detail(self.prescription_id)
        
        if not prescription:
            return
            
        # Update header info
        self.ids.prescription_name.text = prescription.get('name', '')
        self.ids.hospital_name.text = prescription.get('hospital_name', '')
        self.ids.created_date.text = self.format_date(prescription.get('created_at'))
        
        # Load medicines
        medicines_layout = self.ids.medicines_layout
        medicines_layout.clear_widgets()
        
        medicine_details = prescription.get('medicine_details', {})
        for medicine in medicine_details.get('medicines', []):
            self.add_medicine_card(medicine)
    
    def add_medicine_card(self, medicine):
        card = MedicineDetailCard(
            medicine_name=medicine.get('medicine_name', ''),
            usage_time=", ".join(medicine.get('usage_time', [])),
            quantity_per_time=str(medicine.get('quantity_per_time', '')),
            total_quantity=str(medicine.get('total_quantity', '')),
            usage_instruction=medicine.get('usage_instruction', ''),
            duration_days=str(medicine.get('duration_days', '')),
            medicine_info=medicine.get('medicine_info', '')
        )
        self.ids.medicines_layout.add_widget(card)
    
    def format_date(self, date_str):
        try:
            if isinstance(date_str, datetime):
                return date_str.strftime('%d/%m/%Y')
            elif isinstance(date_str, str):
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                return date_obj.strftime('%d/%m/%Y')
            return ''
        except Exception as e:
            print(f"Error parsing date: {e}")
            return ''
            
    def go_back(self):
        self.manager.current = 'history' 