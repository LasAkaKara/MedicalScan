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
from views.screens.python.history_screen import HistoryScreen
from views.screens.python.prescription_detail_screen import PrescriptionDetailScreen
from views.screens.python.scan_screen import ScanScreen
from kivymd.app import MDApp
from services.database_service import DatabaseService

class MedicalApp(MDApp):
    def build(self):
        # Force recreate database (remove this in production)
        if os.path.exists('medical.db'):
            os.remove('medical.db')
            print("Removed old database")
        
        # Initialize database
        db = DatabaseService()
        db.check_database()
        
        self.theme_cls.primary_palette = "Blue"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(VerificationScreen(name='verify'))
        sm.add_widget(HomeScreen(name='medical_home'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(PrescriptionDetailScreen(name='prescription_detail'))
        sm.add_widget(ScanScreen(name='scan'))
        return sm

if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '700')
    Config.set('graphics', 'resizable', False)
    Config.write()
    
    app = MedicalApp()
    app.run() 