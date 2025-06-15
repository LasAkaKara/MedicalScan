from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMessageBox
from views.screens.pyside.prescription_confirm_screen_ui import PrescriptionConfirmScreenUI
from services.database_service import DatabaseService
import logging

logger = logging.getLogger(__name__)

class PrescriptionConfirmScreen(PrescriptionConfirmScreenUI):
    go_back_to_scan = Signal()
    go_to_prescription = Signal()
    
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.db = DatabaseService()
        self.prescription_data = None
        
        # Connect signals
        self.back_btn.clicked.connect(self.handle_back)
        self.cancel_btn.clicked.connect(self.handle_cancel)
        self.save_btn.clicked.connect(self.handle_save)
        self.add_medicine_btn.clicked.connect(self.handle_add_medicine)
    
    def set_prescription_data(self, prescription_data):
        """Set the prescription data to be confirmed"""
        logger.info("Setting prescription data for confirmation")
        logger.debug(f"Prescription data: {prescription_data}")
        
        self.prescription_data = prescription_data
        super().set_prescription_data(prescription_data)
    
    def handle_back(self):
        """Handle back button click"""
        self.go_back_to_scan.emit()
    
    def handle_cancel(self):
        """Handle cancel button click"""
        reply = QMessageBox.question(
            self,
            "Hủy xác nhận",
            "Bạn có chắc chắn muốn hủy? Tất cả thay đổi sẽ bị mất.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.go_back_to_scan.emit()
    
    def handle_add_medicine(self):
        """Handle add medicine button click"""
        self.add_medicine_card()
    
    def handle_save(self):
        """Handle save button click - NOW ACTUALLY SAVES TO DATABASE"""
        try:
            logger.info("Starting prescription save process")
            
            # Get updated prescription data from UI
            updated_data = self.get_prescription_data()
            logger.debug(f"Updated data from UI: {updated_data}")
            
            # Validate required fields
            if not updated_data.get('medicines'):
                QMessageBox.warning(
                    self,
                    "Thiếu thông tin",
                    "Vui lòng thêm ít nhất một loại thuốc."
                )
                return

            # Check if at least one medicine has a name
            has_valid_medicine = any(
                med.get('medicine_name', '').strip() 
                for med in updated_data.get('medicines', [])
            )
            
            if not has_valid_medicine:
                QMessageBox.warning(
                    self,
                    "Thiếu thông tin",
                    "Vui lòng nhập tên thuốc cho ít nhất một loại thuốc."
                )
                return

            # Generate prescription name
            prescription_name = self.generate_prescription_name(updated_data)
            logger.info(f"Generated prescription name: {prescription_name}")

            # Save to database
            logger.info("Saving prescription to database...")
            success = self.db.add_prescription(
                user_id=self.app.current_user_id,
                name=prescription_name,
                hospital_name=updated_data.get('hospital_name', 'Không xác định'),
                category_name="Đơn thuốc quét",
                medicine_details=updated_data
            )

            if success:
                logger.info("Prescription saved successfully")
                QMessageBox.information(
                    self,
                    "Thành công",
                    "Đơn thuốc đã được lưu thành công!"
                )
                # Navigate to prescription list
                self.go_to_prescription.emit()
            else:
                logger.error("Failed to save prescription")
                QMessageBox.critical(
                    self,
                    "Lỗi",
                    "Không thể lưu đơn thuốc. Vui lòng thử lại."
                )

        except Exception as e:
            logger.error(f"Error saving prescription: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Đã xảy ra lỗi khi lưu đơn thuốc: {str(e)}"
            )
    
    def generate_prescription_name(self, prescription_data):
        """Generate a meaningful prescription name"""
        try:
            # Try to use diagnosis first
            diagnosis = prescription_data.get("diagnosis", "").strip()
            if diagnosis:
                return f"Đơn thuốc - {diagnosis}"
            
            # Try to use first medicine name
            medicines = prescription_data.get("medicines", [])
            if medicines:
                first_medicine = medicines[0].get("medicine_name", "").strip()
                if first_medicine:
                    return f"Đơn thuốc - {first_medicine}"
            
            # Fallback to date-based name
            from datetime import datetime
            current_date = datetime.now().strftime("%d/%m/%Y")
            return f"Đơn thuốc quét - {current_date}"
            
        except Exception as e:
            logger.error(f"Error generating prescription name: {e}")
            from datetime import datetime
            return f"Đơn thuốc quét - {datetime.now().strftime('%d/%m/%Y')}"