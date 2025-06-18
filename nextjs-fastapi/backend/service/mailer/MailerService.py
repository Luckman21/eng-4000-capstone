import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from dotenv import load_dotenv

load_dotenv()


class _MailerService:
    def __init__(self):
        api_key = os.getenv('SENDGRID_API_KEY')
        if not api_key:
            raise ValueError("SENDGRID_API_KEY is missing.")
        self.sg = sendgrid.SendGridAPIClient(api_key=api_key)

    def send_email(self, to_addr, subject, body, from_addr):
        from_email = Email(from_addr)
        to_email = To(to_addr)
        content = Content("text/html", body)
        mail = Mail(from_email, to_email, subject, content)

        try:
            response = self.sg.send(mail)
            print(f"Email sent successfully! Response code: {response.status_code}")
        except Exception as e:
            print(f"Error sending email: {e}")