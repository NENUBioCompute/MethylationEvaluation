import smtplib
from email.mime.text import MIMEText
from email.header import Header


class MailSender:
    def __init__(self, smtp_server, username, password):
        self.smtp_server = smtp_server
        self.username = username
        self.password = password

    def send(self, to_addr, subject, content):
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = self.username
        msg['To'] = to_addr
        msg['Subject'] = Header(subject, 'utf-8').encode()
        server = smtplib.SMTP(self.smtp_server, 25)
        server.login(self.username, self.password)
        server.sendmail(self.username, to_addr, msg.as_string())
        server.quit()