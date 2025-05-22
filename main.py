import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from views.screens.python.login_screen import LoginScreen
from views.screens.python.signup_screen import SignupScreen
from views.screens.python.verification_screen import VerificationScreen
from views.screens.python.reset_password_screen import ResetPasswordScreen
from views.screens.python.home_screen import HomeScreen
from views.screens.python.history_screen import HistoryScreen
from views.screens.python.prescription_detail_screen import PrescriptionDetailScreen
from views.screens.python.scan_screen import ScanScreen
from views.screens.python.settings_screen import SettingsScreen
from views.screens.python.profile_screen import ProfileScreen
from kivymd.app import MDApp
from services.database_service import DatabaseService
from controllers.db_controller import DatabaseController

class MedicalApp(MDApp):
    def build(self):
        # Force recreate database (remove this in production)
        if os.path.exists('medical.db'):
            os.remove('medical.db')
            print("Removed old database")
        
        # Initialize database
        self.db_service = DatabaseService()
        self.db_service.check_database()
        
        # Also initialize the controller
        self.db_controller = DatabaseController('app.db')
        self.db_controller.create_tables()
        
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(VerificationScreen(name='verify'))
        sm.add_widget(ResetPasswordScreen(name='reset_password'))
        sm.add_widget(HomeScreen(name='medical_home'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(PrescriptionDetailScreen(name='prescription_detail'))
        sm.add_widget(ScanScreen(name='scan'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(ProfileScreen(name='profile'))
        return sm

    def on_stop(self):
        # Close database connections
        if hasattr(self, 'db_service'):
            self.db_service.close()
        if hasattr(self, 'db_controller'):
            self.db_controller.close()

if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '700')
    Config.set('graphics', 'resizable', False)
    Config.write()
    
    app = MedicalApp()
    app.run() 