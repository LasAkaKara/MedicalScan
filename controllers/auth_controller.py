from models.user import User
from services.database_service import DatabaseService
from services.email_service import EmailService

class AuthController:
    def __init__(self):
        self.db_service = DatabaseService()
        self.email_service = EmailService()

    def login(self, email, password):
        if not email or not password:
            return False, "Vui lòng điền đầy đủ thông tin"
        
        if self.db_service.validate_user(email, password):
            return True, None
        return False, "Email hoặc mật khẩu không đúng"

    def register(self, email, password, confirm_password):
        if not self.validate_registration(email, password, confirm_password):
            return False, "Dữ liệu không hợp lệ"

        verification_code = self.email_service.send_verification_email(email)
        if not verification_code:
            return False, "Không thể gửi mã xác thực"

        if self.db_service.register_user(email, password, verification_code):
            return True, verification_code
        return False, "Email đã tồn tại"

    def verify_code(self, email, code):
        if not code:
            return False, "Vui lòng nhập mã xác thực"

        if self.db_service.verify_code(email, code):
            return True, None
        return False, "Mã xác thực không đúng hoặc đã hết hạn"

    def resend_verification(self, email):
        new_code = self.email_service.send_verification_email(email)
        if new_code and self.db_service.update_verification_code(email, new_code):
            return True, "Đã gửi lại mã xác thực mới"
        return False, "Không thể gửi lại mã xác thực"

    def validate_registration(self, email, password, confirm_password):
        if not email or not password or not confirm_password:
            return False
        if not self.validate_email(email):
            return False
        if len(password) < 6:
            return False
        if password != confirm_password:
            return False
        return True

    def validate_email(self, email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def check_email_exists(self, email):
        """Check if email already exists in the database without sending verification code"""
        if not email or not self.validate_email(email):
            return True  # Return True (exists) for invalid emails to prevent further processing
            
        return self.db_service.email_exists(email)
        
    def send_reset_password_code(self, email):
        """Send a password reset verification code"""
        if not email or not self.validate_email(email):
            return False, "Email không hợp lệ"
            
        # Check if user exists
        if not self.db_service.email_exists(email):
            return False, "Email không tồn tại trong hệ thống"
            
        # Generate and send reset code
        reset_code = self.email_service.send_reset_password_email(email)
        if not reset_code:
            return False, "Không thể gửi mã xác thực"
            
        # Save reset code in database
        if self.db_service.save_reset_code(email, reset_code):
            return True, "Đã gửi mã xác thực"
        return False, "Không thể lưu mã xác thực"
        
    def reset_password(self, email, code, new_password):
        """Reset the user's password using verification code"""
        if not email or not code or not new_password:
            return False, "Vui lòng điền đầy đủ thông tin"
            
        if len(new_password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự"
            
        # Verify the reset code
        if not self.db_service.verify_reset_code(email, code):
            return False, "Mã xác thực không đúng hoặc đã hết hạn"
            
        # Reset the password
        if self.db_service.update_password(email, new_password):
            return True, "Đặt lại mật khẩu thành công"
        return False, "Không thể cập nhật mật khẩu" 