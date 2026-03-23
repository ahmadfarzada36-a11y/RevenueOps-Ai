import smtplib
from email.mime.text import MIMEText
from app.core.config import settings


def send_email(to_email, subject, body):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_USER
    msg["To"] = to_email

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:

        server.starttls()

        server.login(
            settings.EMAIL_USER,
            settings.EMAIL_PASSWORD
        )

        server.send_message(msg)