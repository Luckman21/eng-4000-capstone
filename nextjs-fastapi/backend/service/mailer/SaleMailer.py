from backend.service.mailer.MailerService import _MailerService


class SaleMailer:
    def __init__(self, from_addr):
        self.from_addr = from_addr
        self.client = _MailerService()

    def send_notification(self, to_addr, sale_materials):
        subject = "Pantheon Inventory Management: Inventory Sale Found"
        body = f"Well met,<br><br>The following inventory items have sales or special prices: <br>{sale_materials}"

        return self.client.send_email(to_addr, subject, body, self.from_addr)