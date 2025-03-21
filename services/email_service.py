import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('GMAIL_USER')
        self.password = os.getenv('GMAIL_APP_PASSWORD')

        if not self.sender_email or not self.password:
            raise ValueError("Email credentials not found in .env file")

    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))

    def send_verification_email(self, recipient_email):
        if not recipient_email:
            return None
            
        verification_code = self.generate_verification_code()
        
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = "MediScan - Mã Xác Thực"

        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #406D96; text-align: center;">MediScan - Xác thực email</h2>
                    <p>Xin chào,</p>
                    <p>Cảm ơn bạn đã đăng ký tài khoản MediScan. Để hoàn tất quá trình đăng ký, vui lòng sử dụng mã xác thực dưới đây:</p>
                    <div style="text-align: center; padding: 20px;">
                        <h1 style="color: #406D96; letter-spacing: 5px;">{verification_code}</h1>
                    </div>
                    <p>Mã xác thực này sẽ hết hạn sau 5 phút.</p>
                    <p>Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email này.</p>
                    <hr style="border: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #666; font-size: 12px; text-align: center;">
                        Email này được gửi tự động. Vui lòng không trả lời email này.
                    </p>
                </div>
            </body>
        </html>
        """
        
        message.attach(MIMEText(body, "html"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(message)
            server.quit()
            return verification_code
        except Exception as e:
            print(f"Error sending email: {e}")
            return None

    def send_reset_password_email(self, recipient_email, reset_code):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = "MediScan - Đặt lại mật khẩu"

        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #406D96; text-align: center;">MediScan - Đặt lại mật khẩu</h2>
                    <p>Xin chào,</p>
                    <p>Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản của bạn. Vui lòng sử dụng mã dưới đây để đặt lại mật khẩu:</p>
                    <div style="text-align: center; padding: 20px;">
                        <h1 style="color: #406D96; letter-spacing: 5px;">{reset_code}</h1>
                    </div>
                    <p>Mã này sẽ hết hạn sau 5 phút.</p>
                    <p>Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.</p>
                    <hr style="border: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #666; font-size: 12px; text-align: center;">
                        Email này được gửi tự động. Vui lòng không trả lời email này.
                    </p>
                </div>
            </body>
        </html>
        """

        message.attach(MIMEText(body, "html"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(message)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False 