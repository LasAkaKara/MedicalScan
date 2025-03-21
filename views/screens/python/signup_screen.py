from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from controllers.auth_controller import AuthController

class SignupScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm_password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = AuthController()

    def register(self):
        success, message = self.auth_controller.register(
            self.email.text,
            self.ids.password.password_text,
            self.ids.confirm_password.password_text
        )

        if success:
            verify_screen = self.manager.get_screen('verify')
            verify_screen.current_email = self.email.text
            self.manager.current = 'verify'
            self.clear_fields()
        else:
            self.show_error(message)

    def show_error(self, message):
        self.ids.error_label.text = message
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)

    def clear_fields(self):
        self.email.text = ""
        self.ids.password.ids.password_input.text = ""
        self.ids.confirm_password.ids.password_input.text = ""
        self.ids.error_label.text = ""

    def on_password_focus(self, instance):
        Animation(opacity=1 if instance.focus else 0.7, duration=0.2).start(instance.parent.children[0]) 