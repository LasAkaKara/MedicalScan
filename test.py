import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from views.screens.python.login_screen import LoginScreen
from views.screens.python.signup_screen import SignupScreen
from views.screens.python.verification_screen import VerificationScreen
from views.screens.python.home_screen import HomeScreen
from views.screens.python.prescription_screen import HistoryScreen
from views.screens.python.prescription_detail_screen import PrescriptionDetailScreen
from views.screens.python.scan_screen import ScanScreen, CornerMarker
from views.screens.python.reset_password_screen import ResetPasswordScreen
from kivymd.app import MDApp
from services.database_service import DatabaseService
from controllers.auth_controller import AuthController
from kivy.core.window import Window
from kivy.lang import Builder

# Load all KV files
Builder.load_file('styles.kv')
Builder.load_file('views/screens/kv/login_screen.kv')
Builder.load_file('views/screens/kv/signup_screen.kv')
Builder.load_file('views/screens/kv/verification_screen.kv')
Builder.load_file('views/screens/kv/reset_password_screen.kv')
Builder.load_file('views/screens/kv/home_screen.kv')
Builder.load_file('views/screens/kv/history_screen.kv')
Builder.load_file('views/screens/kv/prescription_detail_screen.kv')
Builder.load_file('views/screens/kv/scan_screen.kv')
Builder.load_file('views/components/navigation_bar.kv')

class TestApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"
    
    def build(self):
        # Initialize database
        db = DatabaseService()
        db.check_database()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Create all screens
        login_screen = LoginScreen(name='login')
        signup_screen = SignupScreen(name='signup')
        verify_screen = VerificationScreen(name='verify')
        home_screen = HomeScreen(name='medical_home')
        history_screen = HistoryScreen(name='history')
        prescription_detail = PrescriptionDetailScreen(name='prescription_detail')
        scan_screen = ScanScreen(name='scan')
        reset_password_screen = ResetPasswordScreen(name='reset_password')
        
        # Add all screens to manager
        sm.add_widget(login_screen)
        sm.add_widget(signup_screen)
        sm.add_widget(verify_screen)
        sm.add_widget(home_screen)
        sm.add_widget(history_screen)
        sm.add_widget(prescription_detail)
        sm.add_widget(scan_screen)
        sm.add_widget(reset_password_screen)
        
        # Simulate successful login by setting up home screen
        home_screen.user_email = 'example@mediscan.com'
        
        # Start at home screen first
        sm.current = 'medical_home'
        
        # Schedule transition to scan screen after a short delay
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.transition_to_scan(sm), 0.5)
        
        return sm
    
    def transition_to_scan(self, sm):
        sm.transition.direction = 'left'
        sm.current = 'scan'

if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '700')
    Config.set('graphics', 'resizable', False)
    Config.write()
    
    Window.size = (400, 700)  # Set window size for desktop testing
    TestApp().run() 