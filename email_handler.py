import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

class EmailNotifier:
    def __init__(self):
        self.load_credentials()
        self.last_notification_time = None
        self.notification_cooldown = 3600

    def load_credentials(self):
        load_dotenv()
        
        self.sender_email = os.getenv('SMTP_EMAIL')
        self.sender_password = os.getenv('SMTP_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            self.setup_initial_config()

    def setup_initial_config(self):
        print("\nE-posta yapılandırması gerekiyor.")
        print("Gmail kullanıyorsanız, lütfen 'App Password' oluşturun.")
        print("(https://myaccount.google.com/apppasswords)\n")
        
        self.sender_email = input("Gönderici E-posta adresini girin: ")
        self.sender_password = input("E-posta App Password'ünü girin: ")
        self.recipient_email = input("Alıcı E-posta adresini girin: ")
        
        with open('.env', 'w') as f:
            f.write(f'SMTP_EMAIL={self.sender_email}\n')
            f.write(f'SMTP_PASSWORD={self.sender_password}\n')
            f.write(f'RECIPIENT_EMAIL={self.recipient_email}\n')
        
        print("\nYapılandırma .env dosyasına kaydedildi.")

    def can_send_notification(self):
        if self.last_notification_time is None:
            return True
        
        time_diff = (datetime.now() - self.last_notification_time).total_seconds()
        return time_diff >= self.notification_cooldown

    def send_speed_alert(self, speed_data):
        if not self.can_send_notification():
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = "İnternet Hızı Düşük Uyarısı!"

            body = f"""
            Dikkat! İnternet hızınız belirlenen limitin altına düştü.
            
            Download Hızı: {int(speed_data['download'] / 1_000_000)} Mbps
            Upload Hızı: {int(speed_data['upload'] / 1_000_000)} Mbps
            Ping: {speed_data['ping']:.2f} ms
            Test Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()

            self.last_notification_time = datetime.now()
            return True

        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False 