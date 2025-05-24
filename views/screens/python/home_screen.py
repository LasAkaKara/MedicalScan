from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.app import App

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_email = ""
        self.current_tab = 'home'

    def on_enter(self):
        print(f"Welcome {self.user_email}")

    def show_hello(self):
        popup = Popup(
            title='Hello',
            content=Label(text='Hello World!'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()
    
    def logout(self):
        app = App.get_running_app()
        app.root.current = 'login'