# services/email_service.py

import smtplib
from email.message import EmailMessage
from ..core.config import settings

from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError, SMTPRecipientsRefused, SMTPSenderRefused



class EmailService:
    def __init__(self):
        self.smtp_email = settings.SMTP_EMAIL
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: str = None,
    ):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.smtp_email
        msg["To"] = to_email
        msg.set_content(body_text)

        if body_html:
            msg.add_alternative(body_html, subtype="html")

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=10) as smtp:
                smtp.login(self.smtp_email, self.smtp_password)
                smtp.send_message(msg)
                return True
        except SMTPAuthenticationError as e:
            raise Exception("SMTP Authentication failed. Check your email and password.") from e
        except SMTPConnectError as e:
            raise Exception("Failed to connect to the SMTP server.") from e
        except SMTPRecipientsRefused as e:
            raise Exception(f"The recipient email was refused: {to_email}") from e
        except SMTPSenderRefused as e:
            raise Exception("The sender address was refused.") from e
        except SMTPException as e:
            raise Exception(f"An SMTP error occurred: {str(e)}") from e
        except Exception as e:
            raise Exception(f"Unexpected error while sending email: {str(e)}") from e
        

    def send_otp_email(self, to_email: str, otp: str):
        subject = "Your Verification OTP"
        body_text = f"Your OTP for email verification is: {otp}\n\nThis OTP will expire in 5 minutes."
        body_html = f"""
        <html>
            <body>
                <p>Your OTP for email verification is: <strong>{otp}</strong></p>
                <p>This OTP will expire in 5 minutes.</p>
            </body>
        </html>
        """
        return self.send_email(to_email, subject, body_text, body_html)

    def send_info_email(self, to_email: str, message: str):
        subject = "Important Information"
        body_text = message
        body_html = f"<html><body><p>{message}</p></body></html>"
        self.send_email(to_email, subject, body_text, body_html)
