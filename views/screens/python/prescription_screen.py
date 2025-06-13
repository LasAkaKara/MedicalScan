# from kivy.uix.screenmanager import Screen
# from services.database_service import DatabaseService
# from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
# from kivy.clock import Clock
# from kivymd.uix.card import MDCard
# from kivymd.uix.label import MDLabel
# from kivy.metrics import dp, sp
# from kivy.utils import get_color_from_hex
# import json
# from datetime import datetime
# from kivy.animation import Animation
# from kivy.properties import BooleanProperty


# class PrescriptionCard(MDCard):
#     show_details = BooleanProperty(False)
#     title = StringProperty("")
#     category = StringProperty("")
#     category_color = ListProperty([1, 1, 1, 1])
#     category_text_color = StringProperty("#000000")
#     date = StringProperty("")
#     hospital = StringProperty("")
#     prescription_id = ObjectProperty(None)

#     def truncate_text(self, text, max_words=15):
#         words = text.split()
#         if len(words) > max_words:
#             return ' '.join(words[:max_words]) + '...'
#         return text

#     def on_category(self, instance, value):
#         if value:
#             self.category = self.truncate_text(value)

#     def on_press(self):
#         print(f"Opening prescription {self.prescription_id}")
#         screen = self.parent.parent.parent.parent
#         if hasattr(screen, 'manager'):
#             detail_screen = screen.manager.get_screen('prescription_detail')
#             detail_screen.prescription_id = self.prescription_id
#             screen.manager.current = 'prescription_detail'

#     def toggle_details(self):
#         details = self.ids.details_content
#         if self.show_details:
#             # Show details
#             Animation(height=details.minimum_height, opacity=1, d=0.3).start(details)
#             self.load_medicine_details()
#         else:
#             # Hide details
#             Animation(height=0, opacity=0, d=0.3).start(details)

#     def load_medicine_details(self):
#         medicines_list = self.ids.medicines_list
#         medicines_list.clear_widgets()
        
#         # Get medicine details from database
#         db = DatabaseService()
#         prescription = db.get_prescription_detail(self.prescription_id)
#         if not prescription:
#             return
            
#         medicine_details = prescription.get('medicine_details', {})
#         for medicine in medicine_details.get('medicines', []):
#             medicine_card = self.create_medicine_card(medicine)
#             medicines_list.add_widget(medicine_card)

#     def create_medicine_card(self, medicine):
#         usage_times = medicine.get('usage_time', [])
#         duration_days = medicine.get('duration_days', '')
#         quantity_per_time = medicine.get('quantity_per_time', '')
        
#         # Handle duration_days type checking
#         try:
#             total_days = int(duration_days) if isinstance(duration_days, str) else duration_days
#         except (ValueError, TypeError):
#             total_days = 0
            
#         total_times_per_day = len(usage_times)
        
#         # Calculate total quantity with better type checking
#         total_quantity = ''
#         try:
#             qty = int(quantity_per_time) if isinstance(quantity_per_time, str) else quantity_per_time
#             if isinstance(qty, int) and total_days > 0:
#                 total = qty * total_times_per_day * total_days
#                 total_quantity = str(total)
#         except (ValueError, TypeError):
#             pass

#         return MedicineDetailCard(
#             medicine_name=medicine.get('medicine_name', ''),
#             usage_info=f"{quantity_per_time} viên × {total_times_per_day} lần/ngày",
#             duration=f"{duration_days} ngày",
#             duration_days=str(duration_days),
#             usage_instruction=medicine.get('usage_instruction', ''),
#             usage_time=usage_times,
#             quantity_per_time=str(quantity_per_time),
#             total_quantity=total_quantity
#         )

# class MedicineDetailCard(MDCard):
#     medicine_name = StringProperty("")
#     usage_info = StringProperty("")
#     duration = StringProperty("")
#     duration_days = StringProperty("")
#     usage_instruction = StringProperty("")
#     usage_time = StringProperty("")
#     quantity_per_time = StringProperty("")
#     total_quantity = StringProperty("")

#     def __init__(self, **kwargs):
#         # Extract duration_days before calling super
#         if 'duration' in kwargs:
#             duration = kwargs['duration']
#             if duration.endswith(' ngày'):
#                 kwargs['duration_days'] = duration[:-5]  # Remove " ngày" suffix
        
#         # Extract and format usage_time before calling super
#         if 'usage_time' in kwargs:
#             times = kwargs.pop('usage_time')  # Remove from kwargs
#             if isinstance(times, list):
#                 self.usage_time = 'Thời gian uống: ' + ', '.join(times)
#             else:
#                 self.usage_time = str(times)
#         super().__init__(**kwargs)

# class HistoryScreen(Screen):
#     def on_enter(self):
#         Clock.schedule_once(self.load_prescriptions, 0.1)

#     def format_date(self, date_str):
#         try:
#             if isinstance(date_str, datetime):
#                 return date_str.strftime('%d/%m/%Y')
#             elif isinstance(date_str, str):
#                 date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
#                 return date_obj.strftime('%d/%m/%Y')
#             return ''
#         except Exception as e:
#             print(f"Error parsing date: {e}")
#             return ''

#     def load_prescriptions(self, dt):
#         print("Loading prescriptions...")
#         db = DatabaseService()
        
#         # Use user_id = 3 directly
#         user_id = 3
        
#         prescriptions = db.get_user_prescriptions(user_id)
#         print(f"Fetched prescriptions: {prescriptions}")
        
#         # Get the prescriptions_layout from KV file
#         prescriptions_layout = self.ids.get('prescriptions_layout')
#         if not prescriptions_layout:
#             print("Error: Could not find prescriptions_layout")
#             return
            
#         prescriptions_layout.clear_widgets()
        
#         if not prescriptions:
#             # Add a "No prescriptions" message
#             no_data_label = MDLabel(
#                 text="Không có đơn thuốc nào",
#                 halign="center",
#                 theme_text_color="Secondary"
#             )
#             prescriptions_layout.add_widget(no_data_label)
#             return

#         # Category color mapping
#         category_colors = {
#             'Bệnh mãn tính': {
#                 'bg': [242/255, 243/255, 218/255, 0.8],  # Lighter yellow
#                 'text': '#887A05'
#             },
#             'Điều trị cấp tính': {
#                 'bg': [243/255, 218/255, 218/255, 0.8],  # Lighter red
#                 'text': '#B53335'
#             },
#             'Thực phẩm chức năng': {
#                 'bg': [220/255, 243/255, 218/255, 0.8],  # Lighter green
#                 'text': '#058840'
#             }
#         }

#         for prescription in prescriptions:
#             try:
#                 print(f"Creating card for prescription: {prescription['name']}")
                
#                 category = prescription.get('category_name', 'Không phân loại')
#                 colors = category_colors.get(category, {
#                     'bg': [220/255, 243/255, 218/255, 0.74],
#                     'text': '#058840'
#                 })

#                 card = PrescriptionCard(
#                     title=prescription.get('name', 'Không có tên'),
#                     category=category,
#                     category_color=colors['bg'],
#                     category_text_color=colors['text'],
#                     date=self.format_date(prescription.get('created_at')),
#                     hospital=prescription.get('hospital_name', ''),
#                     prescription_id=prescription.get('id')
#                 )
                
#                 prescriptions_layout.add_widget(card)
#                 print(f"Added card for: {prescription.get('name')}")
#             except Exception as e:
#                 print(f"Error creating prescription card: {e}")
#                 import traceback
#                 traceback.print_exc()

#     def add_prescription(self):
#         print("Adding new prescription")
#         # TODO: Navigate to add prescription screen

#     def search_prescriptions(self, query):
#         print(f"Searching for: {query}")
#         db = DatabaseService()
#         user_id = 3
        
#         # Get all prescriptions
#         prescriptions = db.get_user_prescriptions(user_id)
        
#         # Filter prescriptions based on search query
#         if query:
#             filtered = []
#             query = query.lower()
#             for p in prescriptions:
#                 # Search in name, hospital name, and category
#                 if (query in p.get('name', '').lower() or 
#                     query in p.get('hospital_name', '').lower() or 
#                     query in p.get('category_name', '').lower()):
#                     filtered.append(p)
#             prescriptions = filtered
        
#         # Update UI
#         prescriptions_layout = self.ids.get('prescriptions_layout')
#         if not prescriptions_layout:
#             return
        
#         prescriptions_layout.clear_widgets()
        
#         if not prescriptions:
#             no_data_label = MDLabel(
#                 text="Không tìm thấy đơn thuốc nào",
#                 halign="center",
#                 theme_text_color="Secondary",
#                 font_style="Body1"
#             )
#             prescriptions_layout.add_widget(no_data_label)
#             return

#         # Add prescription cards
#         for prescription in prescriptions:
#             try:
#                 category = prescription.get('category_name', 'Không phân loại')
#                 colors = self.category_colors.get(category, {
#                     'bg': [220/255, 243/255, 218/255, 0.74],
#                     'text': '#058840'
#                 })

#                 card = PrescriptionCard(
#                     title=prescription.get('name', 'Không có tên'),
#                     category=category,
#                     category_color=colors['bg'],
#                     category_text_color=colors['text'],
#                     date=self.format_date(prescription.get('created_at')),
#                     hospital=prescription.get('hospital_name', ''),
#                     prescription_id=prescription.get('id')
#                 )
                
#                 prescriptions_layout.add_widget(card)
#             except Exception as e:
#                 print(f"Error creating prescription card: {e}") 


from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel
from views.screens.pyside.prescription_screen_ui import PrescriptionScreenUI, PrescriptionCard
from services.database_service import DatabaseService
import json

class PrescriptionScreen(PrescriptionScreenUI):
    go_to_add_prescription = Signal()
    go_to_home = Signal()
    go_to_scan = Signal()
    go_to_detail = Signal(dict)
    go_to_notification = Signal()

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.scan_btn.clicked.connect(self.handle_scan)
        self.add_manual_btn.clicked.connect(self.handle_add_prescription)
        self.search_input.textChanged.connect(self.search_prescriptions)
        self.back_btn.clicked.connect(self.handle_back)
        self.bell_btn.clicked.connect(self.go_to_notification.emit)
        self.db = DatabaseService()
        

    def load_prescriptions(self, user_id):
        user_id = self.app.current_user_id
        prescriptions = self.db.get_user_prescriptions(user_id)
        # Parse medicine_details JSON for each prescription
        for p in prescriptions:
            if isinstance(p.get("medicine_details"), str):
                try:
                    p["medicine_details"] = json.loads(p["medicine_details"])
                except Exception:
                    p["medicine_details"] = {"medicines": []}
            p["medicines"] = p["medicine_details"].get("medicines", [])
        # Clear old widgets
        for i in reversed(range(self.prescriptions_layout.count())):
            widget = self.prescriptions_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Add cards
        for p in prescriptions:
            card = PrescriptionCard(p)
            card.view_details.connect(self.handle_view_details)  # <-- Connect the signal here
            self.prescriptions_layout.addWidget(card)

    def search_prescriptions(self, query):
        prescriptions = self.db.get_user_prescriptions(self.user_id)
        if query:
            query = query.lower()
            prescriptions = [
                p for p in prescriptions
                if query in p.get('name', '').lower()
                or query in p.get('hospital_name', '').lower()
                or query in p.get('category_name', '').lower()
            ]
        # self.display_prescriptions(prescriptions)

    def handle_add_prescription(self):
        self.go_to_add_prescription.emit()
    
    def handle_view_details(self, prescription):
        self.go_to_detail.emit(prescription)
    
    def handle_scan(self):
        self.go_to_scan.emit()

    def handle_back(self):
        self.go_to_home.emit()