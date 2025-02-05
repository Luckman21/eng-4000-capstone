from backend.service.mailer.MailerService import _MailerService

class TempPasswordMailer:

    def __init__(self, from_addr):
        self.from_addr = from_addr
        self.client = _MailerService()

    def send_notification(self, to_addr, temp_password ):
        subject = "Pantheon Inventory Management: Your Temporary Password"
        body = f"Well met,\n\nYour temporary password is: {temp_password}\n\nPlease use this password to log in and reset it as soon as possible.\n\nIf you have not requested a change, you can ignore this email."

        # Send the email using the private _MailerService
        return self.client.send_email(to_addr, subject, body, self.from_addr)