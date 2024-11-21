from sqlalchemy.orm import Session
from db.connect import session
import smtplib
from email.mime.text import MIMEText
from time import sleep

THRESHOLD = 50  # 50g threshold

db = session()
poll_freq = 3600

def send_email(material):
    msg = MIMEText(f"{material} is running low.  Remaining: {material.mass}g.")
    msg['Subject'] = 'Low Stock Alert: {mass}'
    #msg['From'] = # create an email account to send from
    #msg['To'] = #set email address to send info to


def quantity_poll(materials):
    for material in materials:
        if material.mass < THRESHOLD:
            send_email(material)

while True:
    quantity_poll()
    sleep(poll_freq)