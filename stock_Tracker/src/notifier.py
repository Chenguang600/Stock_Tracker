import smtplib
from email.mime.text import MIMEText
import os

class EmailNotifier:
    def __init__(self):
        self.sender = os.getenv('EMAIL_SENDER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.receiver = os.getenv('EMAIL_RECEIVER')

    def send(self, subject, content):
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = self.sender
            msg['To'] = self.receiver

            with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
                server.login(self.sender, self.password)
                server.send_message(msg)

            print(f'邮件已发送至 {self.receiver}')
            return True
        except Exception as e:
            print(f'邮件发送失败: {e}')
            return False
