from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from controllers.auth_controller import AuthController

class VerificationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = AuthController()
        self.current_email = ""

    def on_enter(self):
        self.ids.verification_code.text = ""
        self.ids.error_label.text = ""

    def verify_code(self):
        success, message = self.auth_controller.verify_code(
            self.current_email,
            self.ids.verification_code.text.strip()
        )

        if success:
            self.manager.current = 'login'
            self.show_success_dialog()
        else:
            self.show_error(message)

    def resend_code(self):
        if not self.current_email:
            return

        success, message = self.auth_controller.resend_verification(self.current_email)
        self.show_error(message)

    def show_error(self, message):
        self.ids.error_label.text = message
        self.ids.error_label.color = get_color_from_hex('#FF4444')
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)

    def show_success_dialog(self):
        self.ids.error_label.text = "Xác thực thành công!"
        self.ids.error_label.color = get_color_from_hex('#4CAF50')
        Animation(opacity=1, duration=0.3).start(self.ids.error_label) 