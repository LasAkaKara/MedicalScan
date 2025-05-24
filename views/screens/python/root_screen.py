from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawerItem
from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivymd.app import MDApp


class RootWidget(MDNavigationLayout):
    def toggle_nav_drawer(self):
        self.ids.nav_drawer.set_state("toggle")
    
    def switch_screen(self, screen_name):
        screen_manager = self.ids.screen_manager
        # Change transition for login and signup screens
        if screen_name in ("login", "signup"):
            screen_manager.transition = FadeTransition()
        else:
            screen_manager.transition = SlideTransition()

        screen_manager.current = screen_name
        # Close the navigation drawer if it's open
        nav_drawer = self.ids.nav_drawer
        if nav_drawer.state == "open":
            nav_drawer.set_state("close")

        # If logging out to the login screen, set theme to Light
        if screen_name == "login":
            app = MDApp.get_running_app()
            app.theme_cls.theme_style = "Light"

    def toggle_theme(self):
        app = MDApp.get_running_app()
        current_theme = app.theme_cls.theme_style
        app.theme_cls.theme_style = "Light" if current_theme == "Dark" else "Dark"