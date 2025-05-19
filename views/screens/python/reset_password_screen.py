from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from controllers.auth_controller import AuthController
import logging
from threading import Thread

class ResetPasswordScreen(Screen):
    current_email = StringProperty("")
    is_submitting = BooleanProperty(False)
    is_resending = BooleanProperty(False)
    cooldown_seconds = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = AuthController()
        self.logger = logging.getLogger('MediScan.ResetPasswordScreen')
        self.cooldown_timer = None
        
    def on_enter(self):
        """Called when the screen is entered"""
        self.ids.verification_code.text = ""
        self.ids.new_password.ids.password_input.text = ""
        self.ids.confirm_password.ids.password_input.text = ""
        self.ids.error_label.text = ""
        self.is_submitting = False
        self.is_resending = False
        self.cooldown_seconds = 0
        
        # Cancel any existing cooldown timers
        if self.cooldown_timer:
            self.cooldown_timer.cancel()
            self.cooldown_timer = None
            
        # Auto-send verification code on enter
        self.send_reset_code()
    
    def on_leave(self):
        """Called when the screen is exited"""
        # Cancel cooldown timer when leaving screen
        if self.cooldown_timer:
            self.cooldown_timer.cancel()
            self.cooldown_timer = None
    
    def send_reset_code(self):
        """Send password reset verification code to the user's email"""
        # Check if we're in cooldown period
        if self.cooldown_seconds > 0:
            return
            
        # Prevent multiple resend requests
        if self.is_resending:
            return
            
        if not self.current_email:
            self.show_error("Không có email để gửi mã xác thực")
            return
            
        self.is_resending = True
        
        # Disable resend button if it exists
        if hasattr(self.ids, 'resend_button'):
            self.ids.resend_button.disabled = True
            
        try:
            # Start a thread to process the resend in background
            resend_thread = Thread(target=self.process_send_code)
            resend_thread.daemon = True
            resend_thread.start()
            
            # Start cooldown period (60 seconds)
            self.start_cooldown(60)
        except Exception as e:
            self.logger.error(f"Reset code setup error: {str(e)}")
            self.show_error("Không thể gửi mã xác thực")
            self.is_resending = False
            if hasattr(self.ids, 'resend_button'):
                self.ids.resend_button.disabled = False
    
    def process_send_code(self):
        """Process sending reset code in background"""
        try:
            success, message = self.auth_controller.send_reset_password_code(self.current_email)
            
            # Update UI on main thread
            def update_ui(dt):
                if success:
                    self.show_success_message("Đã gửi mã xác thực đến email của bạn")
                else:
                    self.show_error(message)
                self.is_resending = False
            
            Clock.schedule_once(update_ui, 0.1)
        except Exception as e:
            self.logger.error(f"Send reset code error: {str(e)}")
            Clock.schedule_once(lambda dt: self.show_error("Không thể gửi mã xác thực"), 0.1)
            Clock.schedule_once(lambda dt: setattr(self, 'is_resending', False), 0.1)
    
    def reset_password(self):
        """Reset the user's password"""
        # Prevent multiple submissions
        if self.is_submitting:
            return
            
        self.is_submitting = True
        
        # Disable reset button if it exists
        if hasattr(self.ids, 'reset_button'):
            self.ids.reset_button.disabled = True
            
        try:
            # Validate input
            code = self.ids.verification_code.text.strip()
            new_password = self.ids.new_password.password_text
            confirm_password = self.ids.confirm_password.password_text
            
            if not code:
                self.show_error("Vui lòng nhập mã xác thực")
                self.reset_submission_state()
                return
                
            if not new_password:
                self.show_error("Vui lòng nhập mật khẩu mới")
                self.reset_submission_state()
                return
                
            if len(new_password) < 6:
                self.show_error("Mật khẩu phải có ít nhất 6 ký tự")
                self.reset_submission_state()
                return
                
            if new_password != confirm_password:
                self.show_error("Mật khẩu không khớp")
                self.reset_submission_state()
                return
                
            # Process password reset
            success, message = self.auth_controller.reset_password(
                self.current_email,
                code,
                new_password
            )
            
            if success:
                self.show_success_message("Đặt lại mật khẩu thành công")
                # Navigate back to login screen after delay
                Clock.schedule_once(self.go_to_login, 2)
            else:
                self.show_error(message)
                self.reset_submission_state()
        except Exception as e:
            self.logger.error(f"Reset password error: {str(e)}")
            self.show_error("Đã xảy ra lỗi. Vui lòng thử lại sau.")
            self.reset_submission_state()
    
    def reset_submission_state(self):
        """Reset the submission state to allow resubmission"""
        self.is_submitting = False
        if hasattr(self.ids, 'reset_button'):
            self.ids.reset_button.disabled = False
    
    def go_to_login(self, dt=None):
        """Return to the login screen"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'
    
    def start_cooldown(self, seconds):
        """Start a cooldown timer for the resend button"""
        self.cooldown_seconds = seconds
        
        def update_cooldown(dt):
            self.cooldown_seconds -= 1
            if self.cooldown_seconds <= 0:
                if self.cooldown_timer:
                    self.cooldown_timer.cancel()
                    self.cooldown_timer = None
        
        if self.cooldown_timer:
            self.cooldown_timer.cancel()
        
        self.cooldown_timer = Clock.schedule_interval(update_cooldown, 1)
    
    def show_error(self, message):
        """Show error message"""
        self.ids.error_label.text = message
        self.ids.error_label.color = get_color_from_hex('#FF4444')
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)
    
    def show_success_message(self, message):
        """Show success message"""
        self.ids.error_label.text = message
        self.ids.error_label.color = get_color_from_hex('#4CAF50')
        Animation(opacity=1, duration=0.3).start(self.ids.error_label) 