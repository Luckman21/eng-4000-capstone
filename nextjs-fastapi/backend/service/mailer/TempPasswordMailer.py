from backend.service.mailer.MailerService import _MailerService


class TempPasswordMailer:
    def __init__(self, from_addr):
        self.from_addr = from_addr
        self.client = _MailerService()

    def send_notification(self, to_addr, temp_password ):
        subject = "Pantheon Inventory Management: Your Temporary Password"
        body = f"Well met,<br><br>Your temporary password is: {temp_password}<br><br>Please use this password to log in and reset it as soon as possible.<br>If you have not requested a change, you can ignore this email."

        return self.client.send_email(to_addr, subject, body, self.from_addr)