from kivymd.uix.navigationdrawer import MDNavigationLayout

class RootWidget(MDNavigationLayout):
    def toggle_nav_drawer(self):
        self.ids.nav_drawer.set_state("toggle")
    
    def switch_screen(self, screen_name):
        self.ids.screen_manager.current = screen_name
        # Close the navigation drawer if it's open
        nav_drawer = self.ids.nav_drawer
        if nav_drawer.state == "open":
            nav_drawer.set_state("close")