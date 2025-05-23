from kivy.uix.screenmanager import Screen
from views.screens.python.root_screen import RootWidget
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

    def switch_tab(self, tab_name):
        app = App.get_running_app()
        if tab_name == 'history':
            app.root.current = 'history'
        elif tab_name == 'scan':
            app.root.current = 'scan'
        elif tab_name == 'profile':
            app.root.current = 'profile'
        elif tab_name == 'home':
            app.root.current = 'medical_home'
        print(f"Switched to {tab_name} tab") 