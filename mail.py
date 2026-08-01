import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import SMTP_CONFIG


def send_mail(to, subject, body):

    msg = MIMEMultipart()

    msg["From"] = SMTP_CONFIG["from"]
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(
        MIMEText(
            body,
            "plain",
            "utf-8"
        )
    )

    with smtplib.SMTP(
        SMTP_CONFIG["host"],
        SMTP_CONFIG["port"]
    ) as smtp:

        smtp.starttls()

        smtp.login(
            SMTP_CONFIG["user"],
            SMTP_CONFIG["password"]
        )

        smtp.send_message(msg)