from backend.service.mailer.MailerService import _MailerService


class EnviroWarningMailer:
    def __init__(self, from_addr):
        self.from_addr = from_addr
        self.client = _MailerService()

    def send_notification(self, to_addr, enviro_deficiency, shelf_number):
        subject = "Pantheon Inventory Management: Environmental Warning"
        body = f"Well met,<br><br>Shelf {shelf_number} has a {enviro_deficiency} exception. Make sure to check the unit to " \
               f"ensure your product does not spoil. "

        return self.client.send_email(to_addr, subject, body, self.from_addr)