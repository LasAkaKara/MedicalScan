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
from views.screens.python.root_screen import RootWidget
from kivymd.app import MDApp
from kivy.lang import Builder
from services.database_service import DatabaseService
from controllers.db_controller import DatabaseController

class MedicalApp(MDApp):
    def build(self):
        self.load_all_kv_files()
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

        root = RootWidget()
        return root
    
    def load_all_kv_files(self):
        kv_dir = os.path.join(os.path.dirname(__file__), "views", "screens", "kv")
        
        kv_files = [
            "root_screen.kv",
            "login_screen.kv",
            "signup_screen.kv",
            "verification_screen.kv",
            "reset_password_screen.kv",
            "home_screen.kv",
            "history_screen.kv",
            "prescription_detail_screen.kv",
            "scan_screen.kv",
            "settings_screen.kv",
            "profile_screen.kv"
        ]

        for kv_file in kv_files:
            kv_path = os.path.join(kv_dir, kv_file)
            if os.path.exists(kv_path):
                Builder.load_file(kv_path)
            else:
                print(f"❌ KV file not found: {kv_path}")

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