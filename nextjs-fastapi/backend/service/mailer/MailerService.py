import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import os


class _MailerService:

    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

    def send_email(self, to_addr, subject, body, from_addr):
        from_email = Email(from_addr)
        to_email = To(to_addr)
        content = Content("text/plain", body)
        mail = Mail(from_email, to_email, subject, content)

        try:
            response = self.sg.send(mail)
            print(f"Email sent successfully! Response code: {response.status_code}")
        except Exception as e:
            print(f"Error sending email: {e}")