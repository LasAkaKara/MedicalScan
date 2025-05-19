from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.animation import Animation
from controllers.auth_controller import AuthController
from kivymd.uix.snackbar import Snackbar
import logging
import webbrowser
import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv() # Load environment variables from .env file

class LoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    is_submitting = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = AuthController()
        self.logger = logging.getLogger('MediScan.LoginScreen')

    def validate_login(self):
        # Prevent multiple submissions
        if self.is_submitting:
            return
            
        # Disable submission while processing
        self.is_submitting = True
        
        # Disable login button
        if hasattr(self.ids, 'login_button'):
            self.ids.login_button.disabled = True
        
        try:
            if not self.email.text or not self.ids.password.password_text:
                self.show_error("Vui lòng điền đầy đủ thông tin")
                return
                
            # Check if the email is registered but not verified
            email_status = self.check_email_verification_status(self.email.text)
            
            if email_status == "unverified":
                # Redirect to verification screen
                self.logger.info(f"User {self.email.text} needs verification, redirecting to verification screen")
                self.go_to_verify()
                return
                
            # Normal login flow
            success, message = self.auth_controller.login(
                self.email.text, 
                self.ids.password.password_text
            )
            
            if success:
                home_screen = self.manager.get_screen('medical_home')
                home_screen.user_email = self.email.text
                self.manager.transition.direction = 'left'
                self.manager.current = 'medical_home'
                self.clear_fields()
            else:
                self.show_error(message)
        except Exception as e:
            self.logger.error(f"Login error: {str(e)}")
            self.show_error("Đã xảy ra lỗi. Vui lòng thử lại sau.")
        finally:
            # Re-enable submission
            self.is_submitting = False
            # Re-enable login button
            if hasattr(self.ids, 'login_button'):
                self.ids.login_button.disabled = False

    def check_email_verification_status(self, email):
        """Check if the email is registered but not verified"""
        try:
            # Check if the user exists but is not verified
            if hasattr(self.auth_controller.db_service, 'check_verification_status'):
                return self.auth_controller.db_service.check_verification_status(email)
            return "unknown"
        except Exception as e:
            self.logger.error(f"Error checking verification status: {str(e)}")
            return "unknown"

    def show_error(self, message):
        self.ids.error_label.text = message
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)

    def clear_fields(self):
        self.email.text = ""
        self.ids.password.ids.password_input.text = ""
        self.ids.error_label.text = ""
        self.is_submitting = False

    def on_password_focus(self, instance):
        Animation(opacity=1 if instance.focus else 0.7, duration=0.2).start(instance.parent.children[0])

    def go_to_verify(self):
        if not self.email.text:
            self.show_error("Vui lòng nhập email để xác thực")
            return
            
        verify_screen = self.manager.get_screen('verify')
        verify_screen.current_email = self.email.text
        self.manager.transition.direction = 'left'
        self.manager.current = 'verify'
        self.clear_fields()
        
    def go_to_reset_password(self):
        """Navigate to the reset password screen"""
        # If email is provided, pass it to the reset password screen
        if not self.email.text:
            self.show_error("Vui lòng nhập email để đặt lại mật khẩu")
            return
            
        # Check if the email exists in the database
        email_status = self.check_email_verification_status(self.email.text)
        if email_status == "not_found":
            self.show_error("Email không tồn tại trong hệ thống")
            return
            
        # Navigate to the reset password screen
        try:
            reset_screen = self.manager.get_screen('reset_password')
            reset_screen.current_email = self.email.text
            self.manager.transition.direction = 'left'
            self.manager.current = 'reset_password'
            self.clear_fields()
        except Exception as e:
            self.logger.error(f"Error navigating to reset password screen: {str(e)}")
            self.show_error("Không thể truy cập trang đặt lại mật khẩu")

    def initiate_google_oauth(self):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

        if not client_id or not redirect_uri:
            self.show_error("Google OAuth chưa được cấu hình.")
            self.logger.error("GOOGLE_CLIENT_ID or GOOGLE_REDIRECT_URI not found in .env")
            return

        # Construct the authorization URL
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile', # Request basic profile and email info
            'access_type': 'offline', # To get a refresh token (optional)
            'prompt': 'consent' # Force user to re-consent (optional)
        }
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

        try:
            webbrowser.open(auth_url)
            # Inform the user they need to copy the code from the browser
            # You might want to display a popup or a label for this.
            Snackbar(text="Vui lòng cấp quyền trong trình duyệt và sao chép mã ủy quyền.").open()
            self.logger.info("Opened Google OAuth URL in browser.")
            # --- TODO: Add UI to accept the pasted code --- 
            # Example: Add a TextInput and a Button to submit the code

        except Exception as e:
            self.logger.error(f"Failed to open browser for Google OAuth: {e}")
            self.show_error("Không thể mở trình duyệt để đăng nhập Google.")

    # --- TODO: Add a method to handle the received code --- 
    # Example: def process_google_code(self, code):
    #              This method would send the code to your backend API.