# from kivy.uix.screenmanager import Screen
# from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
# from kivy.clock import Clock
# from kivymd.uix.snackbar import MDSnackbar
# from kivymd.uix.label import MDLabel
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.button import MDRaisedButton
# import os
# import json
# import logging

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# class SettingsScreen(Screen):
#     # Camera settings
#     camera_flip_horizontal = BooleanProperty(False)
#     camera_flip_vertical = BooleanProperty(False)
#     camera_resolution = StringProperty('640x480')
#     camera_quality = NumericProperty(80)  # JPEG quality 0-100
    
#     # App settings
#     auto_detect_documents = BooleanProperty(True)
#     save_original_images = BooleanProperty(False)
#     default_save_folder = StringProperty('prescriptions')
    
#     # Theme settings
#     dark_mode = BooleanProperty(False)
#     accent_color = StringProperty('#2196F3')  # Material Blue
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         logger.debug("Initializing SettingsScreen")
#         self.settings_file = 'app_settings.json'
#         Clock.schedule_once(self.load_settings, 0.1)
    
#     def load_settings(self, dt=None):
#         """Load settings from file"""
#         try:
#             if os.path.exists(self.settings_file):
#                 with open(self.settings_file, 'r') as f:
#                     settings = json.load(f)
                    
#                     # Camera settings
#                     self.camera_flip_horizontal = settings.get('camera_flip_horizontal', False)
#                     self.camera_flip_vertical = settings.get('camera_flip_vertical', False)
#                     self.camera_resolution = settings.get('camera_resolution', '640x480')
#                     self.camera_quality = settings.get('camera_quality', 80)
                    
#                     # App settings
#                     self.auto_detect_documents = settings.get('auto_detect_documents', True)
#                     self.save_original_images = settings.get('save_original_images', False)
#                     self.default_save_folder = settings.get('default_save_folder', 'prescriptions')
                    
#                     # Theme settings
#                     self.dark_mode = settings.get('dark_mode', False)
#                     self.accent_color = settings.get('accent_color', '#2196F3')
                    
#                     logger.debug("Settings loaded successfully")
#             else:
#                 logger.debug("No settings file found, using defaults")
#                 self.save_settings()
#         except Exception as e:
#             logger.error(f"Error loading settings: {e}")
#             self.save_settings()  # Save default settings
    
#     def save_settings(self):
#         """Save settings to file"""
#         try:
#             settings = {
#                 # Camera settings
#                 'camera_flip_horizontal': self.camera_flip_horizontal,
#                 'camera_flip_vertical': self.camera_flip_vertical,
#                 'camera_resolution': self.camera_resolution,
#                 'camera_quality': self.camera_quality,
                
#                 # App settings
#                 'auto_detect_documents': self.auto_detect_documents,
#                 'save_original_images': self.save_original_images,
#                 'default_save_folder': self.default_save_folder,
                
#                 # Theme settings
#                 'dark_mode': self.dark_mode,
#                 'accent_color': self.accent_color
#             }
            
#             with open(self.settings_file, 'w') as f:
#                 json.dump(settings, f, indent=4)
            
#             logger.debug("Settings saved successfully")
#             MDSnackbar(
#                 MDLabel(text="Settings saved"),
#                 duration=1
#             ).open()
#         except Exception as e:
#             logger.error(f"Error saving settings: {e}")
#             self.show_error_dialog("Save Error", f"Failed to save settings: {str(e)}")
    
#     def toggle_camera_flip_horizontal(self):
#         """Toggle horizontal camera flip"""
#         self.camera_flip_horizontal = not self.camera_flip_horizontal
#         self.save_settings()
#         # Show feedback to the user
#         MDSnackbar(MDLabel(text="Horizontal flip " + ("enabled" if self.camera_flip_horizontal else "disabled")), duration=1).open()
    
#     def toggle_camera_flip_vertical(self):
#         """Toggle vertical camera flip"""
#         self.camera_flip_vertical = not self.camera_flip_vertical
#         self.save_settings()
#         # Show feedback to the user
#         MDSnackbar(
#             MDLabel(text="Vertical flip " + ("enabled" if self.camera_flip_vertical else "disabled")), 
#             duration=1).open()
    
#     def set_camera_resolution(self, resolution):
#         """Set camera resolution"""
#         if resolution != self.camera_resolution:
#             self.camera_resolution = resolution
#             self.save_settings()
#             MDSnackbar(MDLabel(text=f"Camera resolution set to {resolution}"), duration=1).open()
#             # Inform the user they need to restart the camera
#             Clock.schedule_once(lambda dt: MDSnackbar(
#                 MDLabel(text="Please restart camera to apply new resolution"), 
#                 duration=2
#             ).open(), 1.5)
    
#     def set_camera_quality(self, quality):
#         """Set camera quality"""
#         self.camera_quality = int(quality)
#         self.save_settings()
    
#     def toggle_auto_detect_documents(self):
#         """Toggle auto-detect documents"""
#         self.auto_detect_documents = not self.auto_detect_documents
#         self.save_settings()
    
#     def toggle_save_original_images(self):
#         """Toggle save original images"""
#         self.save_original_images = not self.save_original_images
#         self.save_settings()
    
#     def set_default_save_folder(self, folder):
#         """Set default save folder"""
#         if os.path.exists(folder):
#             self.default_save_folder = folder
#             self.save_settings()
#         else:
#             # Try to create the folder
#             try:
#                 os.makedirs(folder)
#                 self.default_save_folder = folder
#                 self.save_settings()
#             except Exception as e:
#                 logger.error(f"Error creating folder: {e}")
#                 self.show_error_dialog("Folder Error", f"Failed to create folder: {str(e)}")
    
#     def toggle_dark_mode(self):
#         """Toggle dark mode"""
#         self.dark_mode = not self.dark_mode
#         self.save_settings()
#         # TODO: Update app theme
    
#     def set_accent_color(self, color):
#         """Set accent color"""
#         self.accent_color = color
#         self.save_settings()
#         # TODO: Update app theme
    
#     def show_error_dialog(self, title, message):
#         """Show error dialog"""
#         dialog = MDDialog(
#             title=title,
#             text=message,
#             buttons=[
#                 MDRaisedButton(
#                     text="OK",
#                     on_release=lambda x: dialog.dismiss()
#                 )
#             ]
#         )
#         dialog.open() 

import os
import json
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMessageBox
from views.screens.pyside.settings_screen_ui import SettingsScreenUI
from services.database_service import DatabaseService
from views.components.switch import QSwitch

class SettingsScreen(SettingsScreenUI):
    go_to_home = Signal()

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.db = DatabaseService()
        self.save_btn.clicked.connect(self.save_settings)
        self.back_btn.clicked.connect(self.handle_back)
        self.load_settings()

    def load_settings(self):
        # Get current user info from main app
        user_id = self.app.current_user_id
        user = self.db.get_user_by_id(user_id)
        self.current_user = user
        # Load preferences from DB
        prefs = {}
        if user and user.get("preferences"):
            try:
                prefs = json.loads(user["preferences"])
            except Exception:
                prefs = {}
        # Set UI values
        self.res_combo.setCurrentText(prefs.get('camera_resolution', '640x480'))
        self.quality_slider.setValue(prefs.get('camera_quality', 80))
        self.auto_detect_switch.setChecked(prefs.get('auto_detect_documents', True))
        self.save_original_switch.setChecked(prefs.get('save_original_images', False))
        self.dark_mode_switch.setChecked(prefs.get('dark_mode', False))
        # Notification times
        notif_times = prefs.get("notification_times", {})
        self.time_morning.setTime(self._parse_time(notif_times.get("Sáng", "07:00")))
        self.time_noon.setTime(self._parse_time(notif_times.get("Trưa", "12:00")))
        self.time_evening.setTime(self._parse_time(notif_times.get("Tối", "19:00")))


    def _parse_time(self, tstr):
        from PySide6.QtCore import QTime
        try:
            h, m = map(int, tstr.split(":"))
            return QTime(h, m)
        except Exception:
            return QTime(7, 0)

    def save_settings(self):
        if not self.current_user:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy người dùng hiện tại.")
            return
        # Load existing preferences to preserve other settings
        prefs = {}
        if self.current_user.get("preferences"):
            try:
                prefs = json.loads(self.current_user["preferences"])
            except Exception:
                prefs = {}
        # Update only the relevant settings
        prefs['camera_resolution'] = self.res_combo.currentText()
        prefs['camera_quality'] = self.quality_slider.value()
        prefs['auto_detect_documents'] = self.auto_detect_switch.isChecked()
        prefs['save_original_images'] = self.save_original_switch.isChecked()
        prefs['dark_mode'] = self.dark_mode_switch.isChecked()
        prefs['notification_times'] = {
            "Sáng": self.time_morning.time().toString("HH:mm"),
            "Trưa": self.time_noon.time().toString("HH:mm"),
            "Tối": self.time_evening.time().toString("HH:mm"),
        }
        # Now save back to DB
        success = self.db.update_user_preferences(self.current_user["id"], json.dumps(prefs, ensure_ascii=False))
        if success:
            QMessageBox.information(self, "Thành công", "Đã lưu cài đặt.")
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể lưu cài đặt.")

    def handle_back(self):
        self.go_to_home.emit()