from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from controllers.auth_controller import AuthController
from kivy.clock import Clock
import logging

class VerificationScreen(Screen):
    current_email = StringProperty("")
    is_verifying = BooleanProperty(False)
    is_resending = BooleanProperty(False)
    cooldown_seconds = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = AuthController()
        self.logger = logging.getLogger('MediScan.VerificationScreen')
        self.cooldown_timer = None

    def on_enter(self):
        self.ids.verification_code.text = ""
        self.ids.error_label.text = ""
        self.is_verifying = False
        self.is_resending = False
        self.cooldown_seconds = 0
        
        # Cancel any existing cooldown timers
        if self.cooldown_timer:
            self.cooldown_timer.cancel()
            self.cooldown_timer = None
        
        # Auto-send verification code if coming from registration
        if hasattr(self, 'from_registration') and self.from_registration:
            self.resend_code()
            self.from_registration = False

    def on_leave(self):
        # Cancel cooldown timer when leaving screen
        if self.cooldown_timer:
            self.cooldown_timer.cancel()
            self.cooldown_timer = None

    def verify_code(self):
        # Prevent multiple submissions
        if self.is_verifying:
            return
            
        self.is_verifying = True
        
        # Disable verify button if it exists
        if hasattr(self.ids, 'verify_button'):
            self.ids.verify_button.disabled = True
            
        try:
            if not self.ids.verification_code.text.strip():
                self.show_error("Vui lòng nhập mã xác thực")
                return
                
            success, message = self.auth_controller.verify_code(
                self.current_email,
                self.ids.verification_code.text.strip()
            )

            if success:
                self.show_success_dialog()
                # Add a small delay before navigating back to login
                Clock.schedule_once(lambda dt: self.go_to_login(), 1.5)
            else:
                self.show_error(message)
        except Exception as e:
            self.logger.error(f"Verification error: {str(e)}")
            self.show_error("Đã xảy ra lỗi. Vui lòng thử lại sau.")
        finally:
            self.is_verifying = False
            # Re-enable verify button
            if hasattr(self.ids, 'verify_button'):
                self.ids.verify_button.disabled = False

    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'

    def resend_code(self):
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
            from threading import Thread
            resend_thread = Thread(target=self.process_resend)
            resend_thread.daemon = True
            resend_thread.start()
            
            # Start cooldown period (60 seconds)
            self.start_cooldown(60)
        except Exception as e:
            self.logger.error(f"Resend code setup error: {str(e)}")
            self.show_error("Không thể gửi lại mã xác thực")
            self.is_resending = False
            if hasattr(self.ids, 'resend_button'):
                self.ids.resend_button.disabled = False

    def process_resend(self):
        """Process resend verification code in background"""
        try:
            success, message = self.auth_controller.resend_verification(self.current_email)
            
            # Update UI on main thread
            def update_ui(dt):
                if success:
                    self.show_success_message("Đã gửi lại mã xác thực mới")
                else:
                    self.show_error(message)
                self.is_resending = False
            
            Clock.schedule_once(update_ui, 0.1)
        except Exception as e:
            self.logger.error(f"Resend code error: {str(e)}")
            Clock.schedule_once(lambda dt: self.show_error("Không thể gửi lại mã xác thực"), 0.1)
            Clock.schedule_once(lambda dt: setattr(self, 'is_resending', False), 0.1)

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
        self.ids.error_label.text = message
        self.ids.error_label.color = get_color_from_hex('#FF4444')
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)

    def show_success_message(self, message):
        self.ids.error_label.text = message
        self.ids.error_label.color = get_color_from_hex('#4CAF50')
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)

    def show_success_dialog(self):
        self.ids.error_label.text = "Xác thực thành công!"
        self.ids.error_label.color = get_color_from_hex('#4CAF50')
        Animation(opacity=1, duration=0.3).start(self.ids.error_label) 