from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.database_service import DatabaseService
from kivy.utils import get_color_from_hex
import json
from datetime import datetime
import os
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.utils import platform
from kivy.logger import Logger


class PrescriptionMedicineCard(MDCard):
    medicine_name = StringProperty("")
    usage_info = StringProperty("")
    total_quantity = StringProperty("")
    duration = StringProperty("")
    usage_instruction = StringProperty("")

class PrescriptionDetailScreen(Screen):
    prescription_id = NumericProperty(None)
    _is_loading = False # Add a flag to prevent concurrent loading
    
    def on_enter(self):
        # Log entry but don't load here anymore
        Logger.info(f"Entering PrescriptionDetailScreen for ID: {self.prescription_id}")
        # We now load based on prescription_id changes
        # If the id is already set when entering, on_prescription_id might have already fired
        # or will fire shortly. If it's None initially, on_prescription_id will fire when set.
        pass 

    def on_prescription_id(self, instance, value):
        """Called automatically when the prescription_id property changes."""
        Logger.info(f"on_prescription_id triggered. New ID: {value}")
        if value is not None and not self._is_loading:
            self.load_prescription_details()
        elif value is None:
             Logger.info("prescription_id is None, clearing layout.")
             medicines_layout = self.ids.get('medicines_layout')
             if medicines_layout:
                 medicines_layout.clear_widgets()
             else:
                 Logger.warning("Could not find medicines_layout to clear when ID became None.")
        else: # value is not None but _is_loading is True
            Logger.warning(f"Skipping load in on_prescription_id because loading is already in progress for ID: {value}")

    def load_prescription_details(self):
        if self._is_loading:
            Logger.warning(f"Attempted to call load_prescription_details while already loading for ID: {self.prescription_id}")
            return
            
        Logger.info(f"Starting load_prescription_details for ID: {self.prescription_id}")
        self._is_loading = True
        
        db = DatabaseService()
        prescription = db.get_prescription_detail(self.prescription_id)
        
        if not prescription:
            Logger.error(f"Prescription not found for ID: {self.prescription_id}")
            self._is_loading = False
            return
            
        # Update header info
        self.ids.prescription_name.text = prescription.get('name', '')
        self.ids.hospital_name.text = prescription.get('hospital_name', '')
        self.ids.created_date.text = self.format_date(prescription.get('created_at'))
        
        # Update status chip
        status = prescription.get('status', 'active')
        status_chip = self.ids.status_chip
        if status == 'active':
            status_chip.text = "Đang điều trị"
            status_chip.icon_color = get_color_from_hex('#12B76A')
            status_chip.text_color = get_color_from_hex('#12B76A')
            status_chip.md_bg_color = get_color_from_hex('#ECFDF3')
        elif status == 'completed':
            status_chip.text = "Đã hoàn thành"
            status_chip.icon_color = get_color_from_hex('#12B76A')
            status_chip.text_color = get_color_from_hex('#12B76A')
            status_chip.md_bg_color = get_color_from_hex('#ECFDF3')
        else:
            status_chip.text = "Đã hủy"
            status_chip.icon_color = get_color_from_hex('#F04438')
            status_chip.text_color = get_color_from_hex('#F04438')
            status_chip.md_bg_color = get_color_from_hex('#FEF3F2')
        
        # Load medicines
        medicines_layout = self.ids.get('medicines_layout')
        if not medicines_layout:
             Logger.error(f"Could not find medicines_layout in ids for ID: {self.prescription_id}")
             self._is_loading = False
             return
             
        Logger.info(f"About to clear widgets in medicines_layout for ID: {self.prescription_id}. Current children: {len(medicines_layout.children)}")
        medicines_layout.clear_widgets()
        Logger.info(f"Finished clearing widgets in medicines_layout for ID: {self.prescription_id}. Current children: {len(medicines_layout.children)}")
        
        medicine_details = prescription.get('medicine_details', {})
        medicines_list = medicine_details.get('medicines', [])
        Logger.info(f"Loading {len(medicines_list)} medicines for prescription ID: {self.prescription_id}")
        
        for index, medicine in enumerate(medicines_list):
            self.add_medicine_card(medicine, index)
            
        Logger.info(f"Finished loading all medicine cards for ID: {self.prescription_id}")
        self._is_loading = False
    
    def add_medicine_card(self, medicine, index):
        Logger.info(f"Adding medicine card {index + 1}: {medicine.get('medicine_name', 'N/A')}")
        Logger.debug(f"Medicine data {index + 1}: {medicine}") 
        
        card = PrescriptionMedicineCard(
            medicine_name=medicine.get('medicine_name', ''),
            usage_info=f"{medicine.get('quantity_per_time', '')} viên/lần, {', '.join(medicine.get('usage_time', []))}",
            total_quantity=str(medicine.get('total_quantity', '')),
            duration=f"{medicine.get('duration_days', '')} ngày",
            usage_instruction=medicine.get('usage_instruction', '')
        )
        self.ids.medicines_layout.add_widget(card)
        Logger.info(f"Successfully added medicine card {index + 1}: {medicine.get('medicine_name', 'N/A')}")
    
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
    
    def print_prescription(self):
        """Print the prescription details"""
        try:
            # Get prescription details
            db = DatabaseService()
            prescription = db.get_prescription_detail(self.prescription_id)
            
            if not prescription:
                return
            
            # Create a temporary file for printing
            temp_file = "prescription_print.html"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(self.generate_print_html(prescription))
            
            # Open the file in the default browser for printing
            if platform == 'win':
                os.startfile(temp_file)
            elif platform == 'macosx':
                os.system(f'open {temp_file}')
            else:
                os.system(f'xdg-open {temp_file}')
                
        except Exception as e:
            Logger.error(f"Error printing prescription: {e}")
            self.show_error_dialog("Không thể in đơn thuốc")
    
    def generate_print_html(self, prescription):
        """Generate HTML for printing"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Đơn thuốc - {prescription.get('name', '')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .info {{ margin-bottom: 20px; }}
                .medicine {{ margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; }}
                .medicine-name {{ font-weight: bold; margin-bottom: 5px; }}
                .medicine-details {{ margin-left: 20px; }}
                @media print {{
                    body {{ margin: 0; }}
                    .no-print {{ display: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Đơn thuốc</h1>
                <h2>{prescription.get('name', '')}</h2>
            </div>
            
            <div class="info">
                <p><strong>Bệnh viện:</strong> {prescription.get('hospital_name', '')}</p>
                <p><strong>Ngày tạo:</strong> {self.format_date(prescription.get('created_at'))}</p>
            </div>
            
            <div class="medicines">
                <h3>Danh sách thuốc:</h3>
        """
        
        medicine_details = prescription.get('medicine_details', {})
        for medicine in medicine_details.get('medicines', []):
            html += f"""
                <div class="medicine">
                    <div class="medicine-name">{medicine.get('medicine_name', '')}</div>
                    <div class="medicine-details">
                        <p><strong>Thời gian uống:</strong> {", ".join(medicine.get('usage_time', []))}</p>
                        <p><strong>Liều dùng:</strong> {medicine.get('quantity_per_time', '')} viên/lần</p>
                        <p><strong>Tổng số lượng:</strong> {medicine.get('total_quantity', '')} viên</p>
                        <p><strong>Thời gian điều trị:</strong> {medicine.get('duration_days', '')} ngày</p>
                        <p><strong>Hướng dẫn sử dụng:</strong> {medicine.get('usage_instruction', '')}</p>
                    </div>
                </div>
            """
        
        html += """
            </div>
            <div class="no-print" style="text-align: center; margin-top: 20px;">
                <button onclick="window.print()">In đơn thuốc</button>
            </div>
        </body>
        </html>
        """
        return html
    
    def share_prescription(self):
        """Share prescription details"""
        try:
            # Get prescription details
            db = DatabaseService()
            prescription = db.get_prescription_detail(self.prescription_id)
            
            if not prescription:
                return
            
            # Create share text
            share_text = f"""Đơn thuốc: {prescription.get('name', '')}
Bệnh viện: {prescription.get('hospital_name', '')}
Ngày tạo: {self.format_date(prescription.get('created_at'))}

Danh sách thuốc:
"""
            
            medicine_details = prescription.get('medicine_details', {})
            for medicine in medicine_details.get('medicines', []):
                share_text += f"""
- {medicine.get('medicine_name', '')}
  + Thời gian uống: {", ".join(medicine.get('usage_time', []))}
  + Liều dùng: {medicine.get('quantity_per_time', '')} viên/lần
  + Tổng số lượng: {medicine.get('total_quantity', '')} viên
  + Thời gian điều trị: {medicine.get('duration_days', '')} ngày
  + Hướng dẫn sử dụng: {medicine.get('usage_instruction', '')}
"""
            
            # Show share dialog
            self.show_share_dialog(share_text)
            
        except Exception as e:
            Logger.error(f"Error sharing prescription: {e}")
            self.show_error_dialog("Không thể chia sẻ đơn thuốc")
    
    def show_share_dialog(self, text):
        """Show dialog with prescription details for sharing"""
        dialog = MDDialog(
            title="Chia sẻ đơn thuốc",
            text=text,
            buttons=[
                MDFlatButton(
                    text="Đóng",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_error_dialog(self, message):
        """Show error dialog"""
        dialog = MDDialog(
            title="Lỗi",
            text=message,
            buttons=[
                MDFlatButton(
                    text="Đóng",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open() 