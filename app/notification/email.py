import os
import time
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

from app.config.settings import settings


class EmailService:
    def __init__(self, from_mail: str, from_passwd: str, server_adr: str):
        self.from_mail = from_mail
        self.from_passwd = from_passwd
        self.server_adr = server_adr

    def send_mail(self, text: str, subject: str, to: str):
        msg = MIMEMultipart()
        msg["From"] = self.from_mail
        msg['To'] = to
        msg["Subject"] = Header(subject, 'utf-8')
        msg["Date"] = formatdate(localtime=True)
        msg.attach(MIMEText(text, 'plain', 'utf-8'))

        smtp = smtplib.SMTP(self.server_adr, 587)
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.from_mail, self.from_passwd)
        smtp.sendmail(self.from_mail, to, msg.as_string())
        smtp.quit()

        # Сохраняем сообщение в исходящие
        imap = imaplib.IMAP4_SSL("imap.yandex.ru", 993, timeout=60)
        imap.login(self.from_mail, self.from_passwd)
        imap.select('Sent')
        imap.append('Sent', None,
                    imaplib.Time2Internaldate(time.time()),
                    msg.as_bytes())


email_service = EmailService(settings.FROM_MAIL, settings.FROM_PASSWD, settings.SERVER_ADR)
