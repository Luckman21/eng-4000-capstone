from backend.service.mailer.MailerService import _MailerService


class PasswordChangeMailer:
    def __init__(self, from_addr):
        self.from_addr = from_addr
        self.client = _MailerService()

    def send_notification(self, to_addr):
        subject = "Pantheon Inventory Management: Password Change Notice"
        body = f"Well met,<br><br>Your password has successfully been changed. If this was not you, please contact a system Super Admin for support."

        return self.client.send_email(to_addr, subject, body, self.from_addr)