from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.animation import Animation
from controllers.auth_controller import AuthController
import logging
from threading import Thread
from kivy.clock import Clock

class SignupScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm_password = ObjectProperty(None)
    is_submitting = BooleanProperty(False)
    is_checking_email = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = AuthController()
        self.logger = logging.getLogger('MediScan.SignupScreen')

    def register(self):
        # Prevent multiple submissions
        if self.is_submitting or self.is_checking_email:
            return
            
        # Set submitting flag
        self.is_submitting = True
        
        # Disable signup button if it exists
        if hasattr(self.ids, 'signup_button'):
            self.ids.signup_button.disabled = True
            
        try:
            # Validate input fields
            if not self.email.text or not self.ids.password.password_text or not self.ids.confirm_password.password_text:
                self.show_error("Vui lòng điền đầy đủ thông tin")
                self.reset_submission_state()
                return
                
            # Validate email format
            if not self.is_valid_email(self.email.text):
                self.show_error("Email không hợp lệ")
                self.reset_submission_state()
                return
                
            # Validate password length
            if len(self.ids.password.password_text) < 6:
                self.show_error("Mật khẩu phải có ít nhất 6 ký tự")
                self.reset_submission_state()
                return
                
            # Validate password match
            if self.ids.password.password_text != self.ids.confirm_password.password_text:
                self.show_error("Mật khẩu không khớp")
                self.reset_submission_state()
                return
            
            # Save credentials for validation
            self.temp_email = self.email.text
            self.temp_password = self.ids.password.password_text
            self.temp_confirm_password = self.ids.confirm_password.password_text
            
            # First check if email exists in database
            self.is_submitting = False
            self.is_checking_email = True
            self.check_email_exists()
        except Exception as e:
            self.logger.error(f"Registration error: {str(e)}")
            self.show_error("Đã xảy ra lỗi. Vui lòng thử lại sau.")
            self.reset_submission_state()
    
    def check_email_exists(self):
        """Check if email already exists in database before proceeding"""
        try:
            # Start a thread to check email existence
            check_thread = Thread(target=self.process_email_check)
            check_thread.daemon = True
            check_thread.start()
        except Exception as e:
            self.logger.error(f"Email check error: {str(e)}")
            self.show_error("Không thể kiểm tra email. Vui lòng thử lại sau.")
            self.reset_submission_state()
    
    def process_email_check(self):
        """Process email existence check in background"""
        try:
            # Check if email exists in database
            email_exists = self.auth_controller.check_email_exists(self.temp_email)
            
            # Handle on main thread
            if email_exists:
                # Email already exists
                Clock.schedule_once(lambda dt: self.show_error("Email đã tồn tại. Vui lòng sử dụng email khác."), 0.1)
                Clock.schedule_once(lambda dt: self.reset_submission_state(), 0.1)
            else:
                # Email doesn't exist, proceed with registration
                Clock.schedule_once(lambda dt: self.proceed_to_verification(), 0.1)
        except Exception as e:
            self.logger.error(f"Email check error: {str(e)}")
            Clock.schedule_once(lambda dt: self.show_error("Không thể kiểm tra email. Vui lòng thử lại sau."), 0.1)
            Clock.schedule_once(lambda dt: self.reset_submission_state(), 0.1)
            
    def proceed_to_verification(self):
        """Proceed to verification screen after confirming email doesn't exist"""
        # Re-enable is_submitting for the registration process
        self.is_checking_email = False
        self.is_submitting = True
        
        # Set email in verification screen
        verify_screen = self.manager.get_screen('verify')
        verify_screen.current_email = self.temp_email
        
        # Set flag to indicate coming from registration
        verify_screen.from_registration = True
        
        # Start registration process in the background
        registration_thread = Thread(target=self.process_registration)
        registration_thread.daemon = True
        registration_thread.start()
        
        # Automatically redirect to verification screen
        self.manager.transition.direction = 'left'
        self.manager.current = 'verify'
        self.clear_fields()
                
    def reset_submission_state(self):
        """Reset the submission state to allow resubmission"""
        self.is_submitting = False
        self.is_checking_email = False
        if hasattr(self.ids, 'signup_button'):
            self.ids.signup_button.disabled = False
            
    def is_valid_email(self, email):
        """Validate email format"""
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
                
    def process_registration(self):
        """Process registration in background to prevent UI blocking"""
        try:
            success, message = self.auth_controller.register(
                self.temp_email,
                self.temp_password,
                self.temp_confirm_password
            )
            
            if not success:
                # If registration fails, we need to show an error on the verification screen
                verify_screen = self.manager.get_screen('verify')
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: verify_screen.show_error(message), 0.5)
        except Exception as e:
            self.logger.error(f"Background registration error: {str(e)}")
        finally:
            # Reset submitting flag
            self.is_submitting = False

    def show_error(self, message):
        self.ids.error_label.text = message
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)

    def clear_fields(self):
        self.email.text = ""
        self.ids.password.ids.password_input.text = ""
        self.ids.confirm_password.ids.password_input.text = ""
        self.ids.error_label.text = ""
        self.is_submitting = False

    def on_password_focus(self, instance):
        Animation(opacity=1 if instance.focus else 0.7, duration=0.2).start(instance.parent.children[0]) 