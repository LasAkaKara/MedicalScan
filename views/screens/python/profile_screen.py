# from kivy.uix.screenmanager import Screen
# from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty, ListProperty
# from kivy.clock import Clock
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.button import MDFlatButton, MDRaisedButton
# from kivymd.uix.snackbar import Snackbar
# from services.database_service import DatabaseService
# import logging
# import re
# from datetime import datetime, timedelta
# import json
# from kivymd.uix.label import MDLabel
# from kivy.metrics import dp
# from kivymd.uix.boxlayout import MDBoxLayout

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# class HealthConditionChip(MDBoxLayout):
#     condition = StringProperty("")
#     callback = ObjectProperty(None)

# class ProfileScreen(Screen):
#     username = StringProperty("")
#     email = StringProperty("")
#     full_name = StringProperty("")
#     phone = StringProperty("")
#     is_editing = BooleanProperty(False)
    
#     # Health stats properties
#     prescription_count = NumericProperty(0)
#     scan_count = NumericProperty(0)
#     last_activity = StringProperty("")
#     health_conditions = ListProperty([])
    
#     # Notification preferences
#     notify_medication = BooleanProperty(True)
#     notify_refills = BooleanProperty(True)
#     notify_appointments = BooleanProperty(False)
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         logger.debug("Initializing ProfileScreen")
#         self.dialog = None
#         # Initialize properties with empty strings to avoid None errors
#         self.username = ""
#         self.email = ""
#         self.full_name = ""
#         self.phone = ""
#         self.health_conditions = []
#         Clock.schedule_once(self.load_user_data, 0.1)
    
#     def on_enter(self):
#         """Called when the screen is entered - refresh data"""
#         Clock.schedule_once(self.load_user_data, 0.1)
#         Clock.schedule_once(self.load_user_stats, 0.2)
    
#     def load_user_data(self, dt=None):
#         """Load user data from database"""
#         try:
#             db = DatabaseService()
#             # Get the current user ID - this would typically come from a session or app state
#             # For now, we'll just get the first user in the database
#             user = db.get_current_user()
            
#             if user:
#                 self.username = user.get('username', '')
#                 self.email = user.get('email', '')
#                 # Ensure full_name and phone are strings, not None
#                 self.full_name = user.get('full_name', '') or ''
#                 self.phone = user.get('phone', '') or ''
                
#                 # Load notification preferences
#                 preferences = user.get('preferences', {})
#                 if isinstance(preferences, str):
#                     try:
#                         preferences = json.loads(preferences)
#                     except:
#                         preferences = {}
                
#                 self.notify_medication = preferences.get('notify_medication', True)
#                 self.notify_refills = preferences.get('notify_refills', True)
#                 self.notify_appointments = preferences.get('notify_appointments', False)
                
#                 # Load health conditions
#                 health_data = user.get('health_data', {})
#                 if isinstance(health_data, str):
#                     try:
#                         health_data = json.loads(health_data)
#                     except:
#                         health_data = {}
                
#                 self.health_conditions = health_data.get('conditions', [])
                
#                 logger.debug(f"Loaded user data for {self.username}")
#             else:
#                 logger.warning("No user data found")
#                 # Set default values if no user found
#                 self.username = "DefaultUser"
#                 self.email = "default@example.com"
#                 self.full_name = ""
#                 self.phone = ""
#                 self.health_conditions = []
#         except Exception as e:
#             logger.error(f"Error loading user data: {e}")
#             # Set default values on error
#             self.username = "DefaultUser"
#             self.email = "default@example.com"
#             self.full_name = ""
#             self.phone = ""
#             self.health_conditions = []
    
#     def load_user_stats(self, dt=None):
#         """Load user statistics"""
#         try:
#             db = DatabaseService()
#             user_id = 2  # This should come from a session or app state
            
#             # Get prescription count
#             conn = db.connect()
#             cursor = conn.cursor(dictionary=True)
            
#             # Count prescriptions
#             cursor.execute("SELECT COUNT(*) as count FROM prescriptions WHERE user_id = %s", (user_id,))
#             result = cursor.fetchone()
#             self.prescription_count = result['count'] if result else 0
            
#             # Get last activity
#             cursor.execute("""
#                 SELECT created_at FROM prescriptions 
#                 WHERE user_id = %s 
#                 ORDER BY created_at DESC LIMIT 1
#             """, (user_id,))
#             result = cursor.fetchone()
#             if result and 'created_at' in result:
#                 last_date = result['created_at']
#                 if isinstance(last_date, datetime):
#                     self.last_activity = last_date.strftime("%d/%m/%Y")
#                 else:
#                     try:
#                         last_date = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")
#                         self.last_activity = last_date.strftime("%d/%m/%Y")
#                     except:
#                         self.last_activity = "Unknown"
#             else:
#                 self.last_activity = "No activity yet"
                
#             # Get scan count (assuming there's a scans table)
#             # This is a placeholder - adjust according to actual database schema
#             try:
#                 cursor.execute("SELECT COUNT(*) as count FROM scans WHERE user_id = %s", (user_id,))
#                 result = cursor.fetchone()
#                 self.scan_count = result['count'] if result else 0
#             except:
#                 # Table might not exist yet
#                 self.scan_count = 0
                
#             cursor.close()
#             conn.close()
            
#         except Exception as e:
#             logger.error(f"Error loading user stats: {e}")
#             self.prescription_count = 0
#             self.scan_count = 0
#             self.last_activity = "Unknown"
    
#     def toggle_edit_mode(self):
#         """Toggle between view and edit mode"""
#         self.dialog = MDDialog(
#             type="custom",
#             content_cls=EditProfileDialog(),
#             buttons=[
#                 MDFlatButton(
#                     text="CANCEL",
#                     on_release=lambda x: self.dialog.dismiss()
#                 ),
#                 MDRaisedButton(
#                     text="SAVE",
#                     on_release=self.save_profile
#                 ),
#             ],
#         )
#         self.dialog.open()
    
#     def save_profile(self):
#         """Save updated profile information"""
#         if not self.validate_fields():
#             return
        
#         try:
#             db = DatabaseService()
            
#             # Get values from input fields
#             if hasattr(self.ids, 'email_field'):
#                 email = self.ids.email_field.text
#             else:
#                 email = self.email
                
#             if hasattr(self.ids, 'full_name_field'):
#                 full_name = self.ids.full_name_field.text
#             else:
#                 full_name = self.full_name
                
#             if hasattr(self.ids, 'phone_field'):
#                 phone = self.ids.phone_field.text
#             else:
#                 phone = self.phone
            
#             # Save notification preferences
#             preferences = {
#                 'notify_medication': self.notify_medication,
#                 'notify_refills': self.notify_refills,
#                 'notify_appointments': self.notify_appointments
#             }
            
#             # Save health conditions
#             health_data = {
#                 'conditions': self.health_conditions
#             }
            
#             # Update user data
#             success = db.update_user_profile(
#                 self.username,
#                 email,
#                 full_name,
#                 phone,
#                 json.dumps(preferences),
#                 json.dumps(health_data)
#             )
            
#             if success:
#                 # Update the properties
#                 self.email = email
#                 self.full_name = full_name
#                 self.phone = phone
                
#                 # Exit edit mode
#                 self.is_editing = False
                
#                 # Show success message
#                 Snackbar(text="Profile updated successfully", duration=2).open()
#                 logger.debug("Profile updated successfully")
#             else:
#                 self.show_error_dialog("Update Error", "Failed to update profile. Please try again.")
#         except Exception as e:
#             logger.error(f"Error saving profile: {e}")
#             self.show_error_dialog("Update Error", f"An error occurred: {str(e)}")
    
#     def toggle_notification(self, preference_name):
#         """Toggle a notification preference"""
#         if preference_name == 'medication':
#             self.notify_medication = not self.notify_medication
#         elif preference_name == 'refills':
#             self.notify_refills = not self.notify_refills
#         elif preference_name == 'appointments':
#             self.notify_appointments = not self.notify_appointments
            
#         # You could save immediately, but for simplicity let's save all changes at once
#         logger.debug(f"Toggled {preference_name} notification to {getattr(self, 'notify_' + preference_name)}")
    
#     def add_health_condition(self):
#         """Show dialog to add a health condition"""
#         self.dialog = MDDialog(
#             title="Add Health Condition",
#             type="custom",
#             content_cls=HealthConditionDialog(),
#             buttons=[
#                 MDFlatButton(
#                     text="CANCEL",
#                     on_release=lambda x: self.dialog.dismiss()
#                 ),
#                 MDRaisedButton(
#                     text="ADD",
#                     on_release=self.save_health_condition
#                 ),
#             ],
#         )
#         self.dialog.open()
    
#     def save_health_condition(self, *args):
#         """Save the health condition from dialog"""
#         content = self.dialog.content_cls
#         condition = content.condition.strip()
        
#         if not condition:
#             content.condition_error = "Please enter a health condition"
#             return
            
#         # Add to the list if not already present
#         if condition not in self.health_conditions:
#             self.health_conditions.append(condition)
            
#         self.dialog.dismiss()
        
#         # Update the UI
#         if hasattr(self.ids, 'health_conditions_container'):
#             self.update_health_conditions_ui()
    
#     def update_health_conditions_ui(self):
#         """Update the health conditions UI"""
#         container = self.ids.health_conditions_container
#         container.clear_widgets()
        
#         if not self.health_conditions:
#             # Add a label for no conditions
#             label = MDLabel(
#                 text="No health conditions added yet",
#                 font_style='Caption',
#                 theme_text_color="Secondary",
#                 size_hint_y=None,
#                 height=dp(30)
#             )
#             container.add_widget(label)
#             return
            
#         # Add chips for each condition
#         for condition in self.health_conditions:
#             chip = HealthConditionChip(
#                 condition=condition,
#                 callback=lambda c=condition: self.remove_health_condition(c),
#                 size_hint_x=None
#             )
#             container.add_widget(chip)
    
#     def remove_health_condition(self, condition):
#         """Remove a health condition"""
#         if condition in self.health_conditions:
#             self.health_conditions.remove(condition)
#             # Update the UI
#             if hasattr(self.ids, 'health_conditions_container'):
#                 self.update_health_conditions_ui()
    
#     def validate_fields(self):
#         """Validate input fields"""
#         # Validate email
#         if hasattr(self.ids, 'email_field'):
#             email = self.ids.email_field.text
#             if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#                 self.show_error_dialog("Validation Error", "Please enter a valid email address.")
#                 return False
        
#         # Validate phone (simple validation)
#         if hasattr(self.ids, 'phone_field'):
#             phone = self.ids.phone_field.text
#             if phone and not re.match(r"^\+?[0-9]{10,15}$", phone):
#                 self.show_error_dialog("Validation Error", "Please enter a valid phone number.")
#                 return False
        
#         return True
    
#     def change_password(self):
#         """Show change password dialog"""
#         self.dialog = MDDialog(
#             title="Change Password",
#             type="custom",
#             content_cls=PasswordChangeDialog(),
#             buttons=[
#                 MDFlatButton(
#                     text="CANCEL",
#                     on_release=lambda x: self.dialog.dismiss()
#                 ),
#                 MDRaisedButton(
#                     text="CHANGE",
#                     on_release=self.do_change_password
#                 ),
#             ],
#         )
#         self.dialog.open()
    
#     def do_change_password(self, *args):
#         """Process password change"""
#         content = self.dialog.content_cls
        
#         # Validate current password
#         if not content.current_password:
#             content.current_password_error = "Current password is required"
#             return
        
#         # Validate new password
#         if not content.new_password:
#             content.new_password_error = "New password is required"
#             return
        
#         # Validate password confirmation
#         if content.new_password != content.confirm_password:
#             content.confirm_password_error = "Passwords do not match"
#             return
        
#         try:
#             db = DatabaseService()
            
#             # Verify current password
#             if not db.verify_password(self.username, content.current_password):
#                 content.current_password_error = "Incorrect current password"
#                 return
            
#             # Update password
#             success = db.update_password(self.username, content.new_password)
            
#             if success:
#                 self.dialog.dismiss()
#                 Snackbar(text="Password updated successfully", duration=2).open()
#                 logger.debug("Password updated successfully")
#             else:
#                 content.current_password_error = "Failed to update password"
#         except Exception as e:
#             logger.error(f"Error changing password: {e}")
#             content.current_password_error = f"An error occurred: {str(e)}"
    
#     def show_error_dialog(self, title, message):
#         """Show error dialog"""
#         error_dialog = MDDialog(
#             title=title,
#             text=message,
#             buttons=[
#                 MDRaisedButton(
#                     text="OK",
#                     on_release=lambda x: error_dialog.dismiss()
#                 )
#             ]
#         )
#         error_dialog.open()

# class PasswordChangeDialog(Screen):
#     current_password = StringProperty("")
#     new_password = StringProperty("")
#     confirm_password = StringProperty("")
    
#     current_password_error = StringProperty("")
#     new_password_error = StringProperty("")
#     confirm_password_error = StringProperty("")

# class EditProfileDialog(Screen):
#     email = StringProperty("")
#     full_name = StringProperty("")
#     phone = StringProperty("")

#     email_error = StringProperty("")
#     full_name_error = StringProperty("")
#     phone_error = StringProperty("")
# class HealthConditionDialog(Screen):
#     condition = StringProperty("")
#     condition_error = StringProperty("")
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.condition = "" 

import json
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QMessageBox, QInputDialog
from views.screens.pyside.profile_screen_ui import ProfileScreenUI, EditProfileModal, ChangePasswordModal
from services.database_service import DatabaseService

class ProfileScreen(ProfileScreenUI):
    go_to_login = Signal()
    go_to_home = Signal()

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.current_email = None
        self.back_btn.clicked.connect(self.handle_back_to_home)
        self.logout_btn.clicked.connect(self.handle_logout)
        self.edit_btn.clicked.connect(self.handle_edit)
        self.change_pw_btn.clicked.connect(self.handle_change_password)
        self.notif_medication.stateChanged.connect(lambda state: self.handle_notif_change("Nhắc thuốc", state))
        self.notif_refills.stateChanged.connect(lambda state: self.handle_notif_change("Nhắc tái đơn", state))
        self.db = DatabaseService()

    def load_user_data(self, email):
        self.current_email = email
        user = self.db.get_user_by_email(email)
        if user:
            self.full_name_label.setText(user.get('full_name') or "User")
            self.email_label.setText(user.get('email') or "Not provided")
            self.prescription_count_label.setText(f"Đơn thuốc: {user.get('prescription_count') or 0}")
            self.scan_count_label.setText(f"Lượt quét: {user.get('scan_count') or 0}")
            # Load notification preferences
            prefs = {}
            if user.get("preferences"):
                try:
                    prefs = json.loads(user["preferences"])
                except Exception:
                    prefs = {}
            self.notif_medication.setChecked(prefs.get('notify_medication', True))
            self.notif_refills.setChecked(prefs.get('notify_refills', True))
        else:
            self.full_name_label.setText("User")
            self.email_label.setText("Not provided")

    def handle_logout(self):
        reply = QMessageBox.question(self, "Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.go_to_login.emit()
    
    def handle_back_to_home(self):
        self.go_to_home.emit()

    def handle_edit(self):
        def save_callback(name, email, phone):
            # Save to DB
            user = self.db.get_user_by_email(self.current_email)
            if not user:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy người dùng.")
                return
            # Use old values if fields are empty
            full_name = name or user.get('full_name') or "User"
            email_val = email or user.get('email')
            phone_val = phone or user.get('phone', "")
            # Keep preferences unchanged
            preferences = user.get('preferences', '{}')
            success = self.db.update_user_profile(
                username=user['email'],
                email=email_val,
                full_name=full_name,
                phone=phone_val,
                preferences=preferences,
            )
            if success:
                QMessageBox.information(self, "Thành công", "Cập nhật thông tin thành công.")
                self.load_user_data(email_val)
            else:
                QMessageBox.critical(self, "Lỗi", "Cập nhật thông tin thất bại.")
        dlg = EditProfileModal(
            self.full_name_label.text(),
            self.email_label.text(),
            "",  # phone if you have it
            save_callback,
            self
        )
        dlg.exec()
    

    def handle_change_password(self):
        def change_callback(current, new, confirm, modal):
            has_error = False
            # Validation
            if not current:
                modal.current_pw_error.setText("Vui lòng nhập mật khẩu hiện tại.")
                has_error = True
                return
            else:
                modal.current_pw_error.setText("")
            if not new:
                modal.new_pw_error.setText("Vui lòng nhập mật khẩu mới.")
                has_error = True
                return
            elif len(new) < 6:
                modal.new_pw_error.setText("Mật khẩu mới phải có ít nhất 6 ký tự.")
                has_error = True
                return
            else:
                modal.new_pw_error.setText("")
            if not confirm:
                modal.confirm_pw_error.setText("Vui lòng xác nhận mật khẩu mới.")
                has_error = True
                return
            elif new != confirm:
                modal.confirm_pw_error.setText("Mật khẩu mới và xác nhận không khớp.")
                has_error = True
                return
            else:
                modal.confirm_pw_error.setText("")

            if has_error:
                return

            # Verify current password
            if not self.current_email:
                modal.current_pw_error.setText("Không tìm thấy người dùng hiện tại.")
                return
            if not self.db.verify_password(self.current_email, current):
                modal.current_pw_error.setText("Mật khẩu hiện tại không đúng.")
                return

            # Update password
            if self.db.update_password(self.current_email, new):
                # Optionally show a toast/snackbar here
                modal.current_pw_error.setStyleSheet("color: #43a047; font-size: 12px; border: none; padding: 0px; margin: 0px; min-width: 0px; min-height: 0px;")
                modal.current_pw_error.setText("Đổi mật khẩu thành công!")
                modal.new_pw_error.setText("")
                modal.confirm_pw_error.setText("")
            else:
                modal.current_pw_error.setText("Không thể đổi mật khẩu. Vui lòng thử lại.")

        dlg = ChangePasswordModal(change_callback, self)
        dlg.exec()

    def handle_notif_change(self, label, is_checked):
        user = self.db.get_user_by_email(self.current_email)
        if not user:
            return
        prefs = {}
        if user.get("preferences"):
            try:
                prefs = json.loads(user["preferences"])
            except Exception:
                prefs = {}
        # Always save both switches' states
        prefs["notify_medication"] = self.notif_medication.isChecked()
        prefs["notify_refills"] = self.notif_refills.isChecked()
        self.db.update_user_preferences(user["id"], json.dumps(prefs, ensure_ascii=False))