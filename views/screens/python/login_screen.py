from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from controllers.auth_controller import AuthController

class LoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = AuthController()

    def validate_login(self):
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

    def show_error(self, message):
        self.ids.error_label.text = message
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)

    def clear_fields(self):
        self.email.text = ""
        self.ids.password.ids.password_input.text = ""
        self.ids.error_label.text = ""

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