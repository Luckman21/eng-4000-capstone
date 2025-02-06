from backend.service.mailer.MailerService import _MailerService

class LowStockMailer:

    def __init__(self, from_addr):
        self.from_addr = from_addr
        self.client = _MailerService()

    def send_notification(self, to_addr, product_type, colour, link ):
        subject = "Pantheon Inventory Management: Low Stock Warning"
        body = f"Well met,\n\n You have 50g left of {colour} {product_type}.\n\n Use {link} to purchase more."

        # Send the email using the private _MailerService
        return self.client.send_email(to_addr, subject, body, self.from_addr)