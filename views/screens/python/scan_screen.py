import os
import cv2
import numpy as np
import time
import logging
import json
from datetime import datetime

from PySide6.QtCore import Signal, QTimer, Qt, QRect, QThread
from PySide6.QtWidgets import QMessageBox, QFileDialog, QProgressDialog, QApplication
from PySide6.QtGui import QImage, QPixmap
from views.screens.pyside.scan_screen_ui import ScanScreenUI
from services.ocr_service import OCRService
from services.ai_analysis_service import AIAnalysisService
from services.database_service import DatabaseService

logger = logging.getLogger(__name__)

class ImageQualityAssessor:
    """Assess image quality for OCR accuracy"""
    
    @staticmethod
    def assess_image_quality(image):
        """Assess overall image quality and return score (0-1) and description"""
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Calculate various quality metrics
            sharpness_score = ImageQualityAssessor._calculate_sharpness(gray)
            brightness_score = ImageQualityAssessor._calculate_brightness(gray)
            contrast_score = ImageQualityAssessor._calculate_contrast(gray)
            noise_score = ImageQualityAssessor._calculate_noise_level(gray)
            
            # Weighted overall score
            overall_score = (
                sharpness_score * 0.4 +
                brightness_score * 0.2 +
                contrast_score * 0.3 +
                noise_score * 0.1
            )
            
            # Generate quality description
            if overall_score >= 0.8:
                quality_text = "Chất lượng: Xuất sắc"
            elif overall_score >= 0.65:
                quality_text = "Chất lượng: Tốt"
            elif overall_score >= 0.5:
                quality_text = "Chất lượng: Khá"
            elif overall_score >= 0.3:
                quality_text = "Chất lượng: Kém"
            else:
                quality_text = "Chất lượng: Rất kém"
            
            return overall_score, quality_text
            
        except Exception as e:
            logger.error(f"Error assessing image quality: {e}")
            return 0.5, "Chất lượng: Không xác định"
    
    @staticmethod
    def _calculate_sharpness(gray):
        """Calculate image sharpness using Laplacian variance"""
        try:
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            # Normalize to 0-1 scale (typical range: 0-2000)
            return min(laplacian_var / 1000.0, 1.0)
        except:
            return 0.5
    
    @staticmethod
    def _calculate_brightness(gray):
        """Calculate brightness appropriateness"""
        try:
            mean_brightness = np.mean(gray)
            # Optimal brightness is around 120-180
            if 120 <= mean_brightness <= 180:
                return 1.0
            elif 80 <= mean_brightness <= 220:
                return 0.7
            else:
                return 0.3
        except:
            return 0.5
    
    @staticmethod
    def _calculate_contrast(gray):
        """Calculate image contrast"""
        try:
            contrast = gray.std()
            # Normalize contrast (typical range: 0-100)
            return min(contrast / 80.0, 1.0)
        except:
            return 0.5
    
    @staticmethod
    def _calculate_noise_level(gray):
        """Calculate noise level (lower noise = higher score)"""
        try:
            # Use bilateral filter to estimate noise
            filtered = cv2.bilateralFilter(gray, 9, 75, 75)
            noise = np.mean(np.abs(gray.astype(float) - filtered.astype(float)))
            # Lower noise is better (invert score)
            return max(0, 1.0 - (noise / 50.0))
        except:
            return 0.5

class PrescriptionAnalysisWorker(QThread):
    """Worker thread for prescription analysis to avoid UI blocking"""
    analysis_completed = Signal(dict)
    analysis_failed = Signal(str)
    progress_updated = Signal(str)

    def __init__(self, image, user_id):
        super().__init__()
        self.image = image
        self.user_id = user_id
        self.ocr_service = OCRService()
        self.ai_service = AIAnalysisService()

    def run(self):
        try:
            # Step 1: Auto-crop to scan zone if needed
            self.progress_updated.emit("Đang cắt ảnh tự động...")
            cropped_image = self._auto_crop_to_prescription(self.image)
            
            # Step 2: Assess and enhance image quality
            self.progress_updated.emit("Đang đánh giá chất lượng ảnh...")
            quality_score, _ = ImageQualityAssessor.assess_image_quality(cropped_image)
            
            if quality_score < 0.4:
                self.progress_updated.emit("Đang cải thiện chất lượng ảnh...")
                cropped_image = self._enhance_low_quality_image(cropped_image)
            
            # Step 3: Extract text using OCR
            self.progress_updated.emit("Đang trích xuất văn bản...")
            extracted_text = self.ocr_service.extract_text_from_image(cropped_image)
            
            if not extracted_text or len(extracted_text.strip()) < 10:
                self.analysis_failed.emit("Không thể trích xuất văn bản từ hình ảnh. Vui lòng chụp lại với ánh sáng tốt hơn và đảm bảo đơn thuốc nằm gọn trong khung quét.")
                return
            
            logger.info(f"Extracted text preview: {extracted_text[:200]}...")
            
            # Step 4: Analyze with AI
            self.progress_updated.emit("Đang phân tích đơn thuốc...")
            prescription_data = self.ai_service.analyze_prescription_text(extracted_text)
            
            if not prescription_data:
                self.analysis_failed.emit("Không thể phân tích đơn thuốc. Vui lòng kiểm tra lại hình ảnh và đảm bảo văn bản rõ ràng.")
                return
            
            # Step 5: Validate and enhance extracted data
            self.progress_updated.emit("Đang xác thực dữ liệu...")
            validated_data = self._validate_and_enhance_data(prescription_data, extracted_text)
            
            # Step 6: Return data for confirmation (DON'T SAVE YET)
            self.progress_updated.emit("Hoàn thành phân tích...")
            logger.info(f"Analysis completed successfully. Found {len(validated_data.get('medicines', []))} medicines")
            
            # Emit the data for confirmation screen
            self.analysis_completed.emit(validated_data)
                
        except Exception as e:
            logger.error(f"Error in prescription analysis: {e}")
            import traceback
            traceback.print_exc()
            self.analysis_failed.emit(f"Lỗi phân tích đơn thuốc: {str(e)}")

    def _auto_crop_to_prescription(self, image):
        """Automatically crop image to focus on prescription area"""
        try:
            # Try to detect document boundaries
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edged = cv2.Canny(blurred, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour (likely the document)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Add some padding
                padding = 20
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(image.shape[1] - x, w + 2 * padding)
                h = min(image.shape[0] - y, h + 2 * padding)
                
                # Crop the image
                cropped = image[y:y+h, x:x+w]
                
                # Ensure minimum size
                if cropped.shape[0] > 200 and cropped.shape[1] > 200:
                    logger.info(f"Auto-cropped image from {image.shape} to {cropped.shape}")
                    return cropped
            
            # If auto-crop fails, return original
            logger.info("Auto-crop failed, using original image")
            return image
            
        except Exception as e:
            logger.error(f"Error in auto-crop: {e}")
            return image

    def _enhance_low_quality_image(self, image):
        """Enhance low quality images for better OCR"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply CLAHE for better contrast
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
            
            # Sharpen
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            # Convert back to BGR if original was color
            if len(image.shape) == 3:
                enhanced_bgr = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)
                return enhanced_bgr
            else:
                return sharpened
                
        except Exception as e:
            logger.error(f"Error enhancing image: {e}")
            return image

    def _validate_and_enhance_data(self, prescription_data, extracted_text):
        """Validate and enhance extracted prescription data"""
        try:
            # Ensure we have at least one medicine
            if not prescription_data.get("medicines"):
                # Try to extract medicine names from text using patterns
                medicine_names = self._extract_medicine_names_from_text(extracted_text)
                if medicine_names:
                    prescription_data["medicines"] = [
                        {
                            "medicine_name": name,
                            "type": "Viên",
                            "strength": "",
                            "total_quantity": "",
                            "quantity_per_time": "1 viên",
                            "duration_days": "7",
                            "usage_instruction": "",
                            "usage_time": [{"time": "Sáng", "quantity": 1}]
                        }
                        for name in medicine_names
                    ]
            
            # Enhance hospital name if missing
            if not prescription_data.get("hospital_name"):
                hospital = self._extract_hospital_from_text(extracted_text)
                if hospital:
                    prescription_data["hospital_name"] = hospital
            
            # Enhance diagnosis if missing
            if not prescription_data.get("diagnosis"):
                diagnosis = self._extract_diagnosis_from_text(extracted_text)
                if diagnosis:
                    prescription_data["diagnosis"] = diagnosis
            
            return prescription_data
            
        except Exception as e:
            logger.error(f"Error validating data: {e}")
            return prescription_data

    def _extract_medicine_names_from_text(self, text):
        """Extract potential medicine names using patterns"""
        import re
        
        # Common medicine name patterns
        patterns = [
            r'\b[A-Z][a-z]+(?:cillin|mycin|zole|prazole|tadine|amine|olol|sartan|statin)\b',
            r'\b(?:Paracetamol|Aspirin|Vitamin|Amoxicillin|Omeprazole|Cetirizine)\b',
            r'\b[A-Z][a-z]+\s+\d+\s*(?:mg|ml|g)\b'
        ]
        
        medicine_names = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            medicine_names.extend(matches)
        
        # Remove duplicates and return first 5
        return list(dict.fromkeys(medicine_names))[:5]

    def _extract_hospital_from_text(self, text):
        """Extract hospital name from text"""
        import re
        
        patterns = [
            r'(?:Bệnh viện|Hospital|Phòng khám|Clinic)\s+([^\n,]+)',
            r'([^\n,]*(?:Hospital|Medical|Clinic|Bệnh viện|Y tế)[^\n,]*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""

    def _extract_diagnosis_from_text(self, text):
        """Extract diagnosis from text"""
        import re
        
        patterns = [
            r'(?:Chẩn đoán|Diagnosis|Bệnh)[:\s]+([^\n,]+)',
            r'(?:Điều trị|Treatment)[:\s]+([^\n,]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""

class ScanScreen(ScanScreenUI):
    go_to_home = Signal()
    go_to_settings = Signal()
    go_to_prescription = Signal()
    go_to_confirm = Signal(dict)  # Signal to navigate to confirmation screen

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.back_btn.clicked.connect(self.handle_back_to_home)
        self.capture_btn.clicked.connect(self.handle_capture)
        self.upload_btn.clicked.connect(self.handle_upload)
        self.retake_btn.clicked.connect(self.handle_retake)
        self.confirm_btn.clicked.connect(self.handle_confirm)
        self.save_btn.clicked.connect(self.handle_save)

        # Camera and image state
        self.camera_initialized = False
        self.capture = None
        self.frame = None
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_camera_frame)
        self.current_image = None
        self.prescriptions_dir = 'prescriptions'
        os.makedirs(self.prescriptions_dir, exist_ok=True)
        
        # Analysis components
        self.analysis_worker = None
        self.progress_dialog = None
        
        # Quality assessment
        self.quality_assessor = ImageQualityAssessor()

    def create_styled_message_box(self, icon, title, text, buttons=QMessageBox.Ok):
        """Create a properly styled message box"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(buttons)
        
        # Apply styling to fix black background issue
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: black;
            }
            QMessageBox QLabel {
                color: black;
                background-color: transparent;
            }
            QMessageBox QPushButton {
                background-color: #0ea5e9;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #0284c7;
            }
            QMessageBox QPushButton:pressed {
                background-color: #0369a1;
            }
        """)
        
        return msg_box

    # --- Camera methods ---
    def start_camera(self):
        if self.camera_initialized:
            return
        try:
            self.capture = cv2.VideoCapture(0)
            if self.capture.isOpened():
                self.camera_initialized = True
                self.camera_timer.start(30)  # ~30 FPS
                logger.info("Camera started successfully")
            else:
                logger.error("Failed to open camera")
                msg_box = self.create_styled_message_box(
                    QMessageBox.Critical,
                    "Camera Error",
                    "Không thể khởi động camera."
                )
                msg_box.exec()
        except Exception as e:
            logger.error(f"Error starting camera: {e}")

    def stop_camera(self):
        if self.camera_initialized and self.capture:
            self.camera_timer.stop()
            self.capture.release()
            self.capture = None
            self.camera_initialized = False
            logger.info("Camera stopped")

    def update_camera_frame(self):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret and frame is not None:
                self.frame = frame
                self.display_camera_frame(frame)
                self.capture_btn.setEnabled(True)
                
                # Assess frame quality in real-time
                quality_score, quality_text = self.quality_assessor.assess_image_quality(frame)
                self.update_quality_indicator(quality_score, quality_text)
            else:
                self.capture_btn.setEnabled(False)
        else:
            self.capture_btn.setEnabled(False)

    def update_quality_indicator(self, quality_score, quality_text):
        """Update the quality indicator based on image analysis"""
        try:
            if hasattr(self, 'quality_indicator'):
                if quality_score >= 0.8:
                    color = "#22c55e"  # Green
                    icon = "✅"
                elif quality_score >= 0.6:
                    color = "#f59e0b"  # Orange
                    icon = "⚠️"
                else:
                    color = "#ef4444"  # Red
                    icon = "❌"
                
                self.quality_indicator.setText(f"{icon} {quality_text}")
                self.quality_indicator.setStyleSheet(f"""
                    background: {color};
                    color: white;
                    padding: 8px 12px;
                    border-radius: 16px;
                    font-size: 12px;
                    font-weight: bold;
                """)
        except Exception as e:
            logger.error(f"Error updating quality indicator: {e}")

    def display_camera_frame(self, frame):
        try:
            # Flip the frame horizontally
            flipped = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
            self.camera_label.setPixmap(
                pixmap.scaled(
                    self.camera_label.width(),
                    self.camera_label.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
            )
        except Exception as e:
            logger.error(f"Error displaying camera frame: {e}")

    def display_image(self, image):
        try:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
            self.camera_label.setPixmap(
                pixmap.scaled(
                    self.camera_label.width(),
                    self.camera_label.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
            )
        except Exception as e:
            logger.error(f"Error displaying image: {e}")

    # --- UI Control methods ---
    def show_capture_controls(self):
        # Show floating capture/upload buttons, hide bottom controls
        if hasattr(self, 'capture_btn'):
            self.capture_btn.show()
        if hasattr(self, 'upload_btn'):
            self.upload_btn.show()
        if hasattr(self, 'bottom_controls'):
            self.bottom_controls.hide()

    def show_post_capture_controls(self, show_save=True):
        # Hide floating capture/upload buttons, show bottom controls
        if hasattr(self, 'capture_btn'):
            self.capture_btn.hide()
        if hasattr(self, 'upload_btn'):
            self.upload_btn.hide()
        if hasattr(self, 'bottom_controls'):
            self.bottom_controls.show()
        if hasattr(self, 'retake_btn'):
            self.retake_btn.show()
        if hasattr(self, 'confirm_btn'):
            self.confirm_btn.show()
        if hasattr(self, 'save_btn'):
            self.save_btn.setVisible(show_save)

    # --- Event handlers ---
    def handle_capture(self):
        if self.frame is not None:
            # Flip horizontally to match preview
            captured = cv2.flip(self.frame, 1)
            self.current_image = captured
            self.stop_camera()
            self.display_image(self.current_image)
            self.show_post_capture_controls(show_save=True)
        else:
            msg_box = self.create_styled_message_box(
                QMessageBox.Warning,
                "Lỗi",
                "Không có khung hình để chụp."
            )
            msg_box.exec()
    
    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Chọn ảnh đơn thuốc", 
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if file_path:
            image = cv2.imread(file_path)
            if image is not None:
                # Assess uploaded image quality
                quality_score, quality_text = self.quality_assessor.assess_image_quality(image)
                
                if quality_score < 0.3:
                    reply = QMessageBox.question(
                        self,
                        "Chất lượng ảnh kém",
                        f"Ảnh được tải lên có chất lượng kém ({quality_text}). "
                        "Điều này có thể ảnh hưởng đến độ chính xác của việc quét. "
                        "Bạn có muốn tiếp tục không?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No
                    )
                    if reply == QMessageBox.No:
                        return
                
                self.current_image = image
                self.stop_camera()
                self.display_image(self.current_image)
                self.show_post_capture_controls(show_save=False)
                self.enable_image_drag()
                
                # Update quality indicator
                self.update_quality_indicator(quality_score, quality_text)
            else:
                msg_box = self.create_styled_message_box(
                    QMessageBox.Warning,
                    "Lỗi",
                    "Không thể mở ảnh. Vui lòng chọn file ảnh hợp lệ."
                )
                msg_box.exec()
    
    def handle_retake(self):
        self.camera_label.clear()
        self.current_image = None
        self.show_capture_controls()
        self.reset_camera_label_drag()
        self.start_camera()

    def handle_save(self):
        if self.current_image is not None:
            timestr = time.strftime("%Y%m%d_%H%M%S")
            filename = f"prescription_{timestr}.png"
            filepath = os.path.join(self.prescriptions_dir, filename)
            cv2.imwrite(filepath, self.current_image)
            msg_box = self.create_styled_message_box(
                QMessageBox.Information,
                "Thành công",
                f"Đã lưu vào {filepath}"
            )
            msg_box.exec()

    def handle_confirm(self):
        """Start prescription analysis workflow"""
        if self.current_image is not None:
            # Show confirmation dialog with proper styling
            msg_box = self.create_styled_message_box(
                QMessageBox.Question,
                "Xác nhận quét",
                "Bạn có muốn phân tích đơn thuốc này không?\n\nHệ thống sẽ:\n1. Trích xuất văn bản từ hình ảnh\n2. Phân tích thông tin đơn thuốc\n3. Hiển thị để bạn xác nhận",
                QMessageBox.Yes | QMessageBox.No
            )
            
            reply = msg_box.exec()
            if reply == QMessageBox.Yes:
                self.start_prescription_analysis()
        else:
            msg_box = self.create_styled_message_box(
                QMessageBox.Warning,
                "Lỗi",
                "Không có hình ảnh để phân tích."
            )
            msg_box.exec()

    def handle_back_to_home(self):
        self.stop_camera()
        if hasattr(self, 'camera_label'):
            self.camera_label.clear()
        self.current_image = None
        self.show_capture_controls()
        self.reset_camera_label_drag()
        self.go_to_home.emit()

    # --- Analysis methods ---
    def start_prescription_analysis(self):
        """Start the prescription analysis process"""
        try:
            # Create progress dialog with styling
            self.progress_dialog = QProgressDialog("Đang khởi tạo...", "Hủy", 0, 0, self)
            self.progress_dialog.setWindowTitle("Phân tích đơn thuốc")
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.canceled.connect(self.cancel_analysis)
            
            # Style the progress dialog
            self.progress_dialog.setStyleSheet("""
                QProgressDialog {
                    background-color: white;
                    color: black;
                }
                QProgressDialog QLabel {
                    color: black;
                    background-color: transparent;
                }
                QProgressDialog QPushButton {
                    background-color: #ef4444;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QProgressDialog QPushButton:hover {
                    background-color: #dc2626;
                }
            """)
            
            # Create and start worker thread
            self.analysis_worker = PrescriptionAnalysisWorker(
                self.current_image.copy(), 
                self.app.current_user_id
            )
            
            # Connect signals
            self.analysis_worker.progress_updated.connect(self.update_analysis_progress)
            self.analysis_worker.analysis_completed.connect(self.on_analysis_completed)
            self.analysis_worker.analysis_failed.connect(self.on_analysis_failed)
            self.analysis_worker.finished.connect(self.cleanup_analysis)
            
            # Start analysis
            self.analysis_worker.start()
            self.progress_dialog.show()
            
        except Exception as e:
            logger.error(f"Error starting prescription analysis: {e}")
            msg_box = self.create_styled_message_box(
                QMessageBox.Critical,
                "Lỗi",
                f"Không thể bắt đầu phân tích: {str(e)}"
            )
            msg_box.exec()

    def update_analysis_progress(self, message):
        """Update progress dialog with current step"""
        if self.progress_dialog:
            self.progress_dialog.setLabelText(message)

    def on_analysis_completed(self, prescription_data):
        """Handle successful prescription analysis"""
        try:
            if self.progress_dialog:
                self.progress_dialog.close()
            
            logger.info("Analysis completed, navigating to confirmation screen")
            logger.debug(f"Prescription data: {prescription_data}")
            
            # Navigate to confirmation screen with the analyzed data
            self.go_to_confirm.emit(prescription_data)
            
        except Exception as e:
            logger.error(f"Error handling analysis completion: {e}")

    def on_analysis_failed(self, error_message):
        """Handle failed prescription analysis"""
        if self.progress_dialog:
            self.progress_dialog.close()
        
        msg_box = self.create_styled_message_box(
            QMessageBox.Critical,
            "Lỗi phân tích",
            f"Không thể phân tích đơn thuốc:\n\n{error_message}\n\nVui lòng thử lại với hình ảnh rõ nét hơn."
        )
        msg_box.exec()

    def cancel_analysis(self):
        """Cancel the ongoing analysis"""
        if self.analysis_worker and self.analysis_worker.isRunning():
            self.analysis_worker.terminate()
            self.analysis_worker.wait()
        
        if self.progress_dialog:
            self.progress_dialog.close()

    def cleanup_analysis(self):
        """Clean up after analysis completion"""
        if self.analysis_worker:
            self.analysis_worker.deleteLater()
            self.analysis_worker = None
        
        if self.progress_dialog:
            self.progress_dialog.deleteLater()
            self.progress_dialog = None

    # --- Image drag methods ---
    def enable_image_drag(self):
        try:
            # Save original handlers if not already saved
            if not hasattr(self.camera_label, "_orig_mousePressEvent"):
                self.camera_label._orig_mousePressEvent = self.camera_label.mousePressEvent
            if not hasattr(self.camera_label, "_orig_mouseMoveEvent"):
                self.camera_label._orig_mouseMoveEvent = self.camera_label.mouseMoveEvent
            if not hasattr(self.camera_label, "_orig_mouseReleaseEvent"):
                self.camera_label._orig_mouseReleaseEvent = self.camera_label.mouseReleaseEvent

            self.camera_label.setCursor(Qt.OpenHandCursor)
            self.camera_label.mousePressEvent = self._drag_start
            self.camera_label.mouseMoveEvent = self._drag_move
            self.camera_label.mouseReleaseEvent = self._drag_end
            self._drag_pos = None
        except Exception as e:
            logger.error(f"Error enabling image drag: {e}")
    
    def reset_camera_label_drag(self):
        try:
            # Restore original event handlers if they exist
            if hasattr(self, 'camera_label'):
                if hasattr(self.camera_label, "_orig_mousePressEvent"):
                    self.camera_label.mousePressEvent = self.camera_label._orig_mousePressEvent
                if hasattr(self.camera_label, "_orig_mouseMoveEvent"):
                    self.camera_label.mouseMoveEvent = self.camera_label._orig_mouseMoveEvent
                if hasattr(self.camera_label, "_orig_mouseReleaseEvent"):
                    self.camera_label.mouseReleaseEvent = self.camera_label._orig_mouseReleaseEvent
                self.camera_label.setCursor(Qt.ArrowCursor)
                self.camera_label.move(0, 0)
        except Exception as e:
            logger.error(f"Error resetting camera label drag: {e}")

    def _drag_start(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.pos()
            self.camera_label.setCursor(Qt.ClosedHandCursor)

    def _drag_move(self, event):
        if self._drag_pos is not None:
            delta = event.pos() - self._drag_pos
            self.camera_label.move(self.camera_label.pos() + delta)

    def _drag_end(self, event):
        self._drag_pos = None
        self.camera_label.setCursor(Qt.OpenHandCursor)

    # --- PySide6 widget events ---
    def showEvent(self, event):
        super().showEvent(event)
        self.start_camera()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.stop_camera()

    def show_capture_guidance(self):
        """Show guidance for better image capture"""
        guidance_msg = """
📸 Hướng dẫn chụp ảnh đơn thuốc chất lượng cao:

✅ Nên làm:
• Đặt đơn thuốc trên bề mặt phẳng, sáng
• Chụp từ trên xuống, vuông góc với đơn thuốc
• Đảm bảo ánh sáng đủ và đều
• Giữ camera ổn định khi chụp
• Đơn thuốc phải nằm gọn trong khung hình
• Chụp ở độ phân giải cao

❌ Tránh:
• Chụp nghiêng hoặc xiên góc
• Ánh sáng quá tối hoặc có bóng đổ
• Camera bị rung lắc
• Đơn thuốc bị cắt xén
• Chụp từ xa quá

💡 Mẹo: Sử dụng đèn bàn hoặc ánh sáng tự nhiên để có kết quả tốt nhất!
        """
        
        msg_box = self.create_styled_message_box(
            QMessageBox.Information,
            "Hướng dẫn chụp ảnh",
            guidance_msg
        )
        msg_box.exec()