
import os
import smtplib
import logging

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_teacher_registration_email(
    teacher_email: str,
    teacher_name: str
):
    try:
        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")

        if not sender_email or not sender_password:
            raise ValueError("Email credentials are missing")

        message = EmailMessage()

        message["Subject"] = "Teacher Registration Successful"
        message["From"] = sender_email
        message["To"] = teacher_email

        message.set_content(
            f"""
Hello {teacher_name},

Your teacher registration was successful.

Welcome to our Teacher Management System!

Thank you.
"""
        )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465
        ) as server:

            server.login(sender_email, sender_password)
            server.send_message(message)

        logger.info(
            "Email successfully sent to %s",
            teacher_email
        )

    except Exception:
        logger.exception(
            "Failed to send email to %s",
            teacher_email
        )
