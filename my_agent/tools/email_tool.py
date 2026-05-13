import smtplib
from email.message import EmailMessage
import os


def send_email(to: str, subject: str, body: str) -> str:
    """
    يرسل بريداً إلكترونياً عبر Gmail.

    Args:
        to: عنوان البريد الإلكتروني للمستلم، مثال: 'example@gmail.com'
        subject: موضوع الرسالة
        body: نص الرسالة
    """
    try:
        sender = os.getenv("GMAIL_ADDRESS")
        password = os.getenv("GMAIL_APP_PASSWORD")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(msg)

        return f" تم إرسال البريد الإلكتروني إلى {to} بنجاح"

    except Exception as e:
        return f"خطأ في إرسال البريد الإلكتروني: {str(e)}"