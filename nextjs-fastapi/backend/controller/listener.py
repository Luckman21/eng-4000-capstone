from sqlalchemy.orm import Session
from db.connect import session
from sqlalchemy import event
import smtplib
from email.mime.text import MIMEText
from time import sleep

THRESHOLD = 50  # 50g threshold

"""
def send_email(material):
    msg = MIMEText(f"{material} is running low.  Remaining: {material.mass}g.")
    msg['Subject'] = 'Low Stock Alert: {material.mass}'
    #msg['From'] = # create an email account to send from
    #msg['To'] = #set email address to send info to
"""

# A polling function to check the mass of each material in the table
def quantity_poll(materials):
    alert = []  # create an array for materials with a mass below 50g

    for material in materials:
        if material.mass < THRESHOLD:
            alert.append(material)

    return alert # return an array of materials with mass below 50g

def job_complete_listener(mRepo):
    materials = mRepo.get_all_materials()
    return quantity_poll(materials)