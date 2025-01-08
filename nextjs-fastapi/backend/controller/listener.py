from db.repositories.MaterialRepository import MaterialRepository
from db import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import smtplib
from email.mime.text import MIMEText
from backend.controller.main import ws_manager

THRESHOLD = 50  # 50g threshold

# Create an engine and local session for connection to the database
engine = create_engine(connect.DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

"""
def send_email(material):
    msg = MIMEText(f"{material} is running low.  Remaining: {material.mass}g.")
    msg['Subject'] = 'Low Stock Alert: {material.mass}'
    #msg['From'] = # create an email account to send from
    #msg['To'] = #set email address to send info to
"""

# A polling function to check the mass of each material in the table
async def quantity_poll(materials):
    """
    A polling function to check the mass of each material in the table, returns an array of materials with a mass below the threshold value.

    Args:
        materials(List[Material]): A list of Material objects to iterate through.

    Returns:
        List[Material]: A list of materials with a mass below the threshold value.
    """
    alert = []  # create an array for materials with a mass below 50g

    # Iterate through all materials, append those with a mass below the threshold value
    for material in materials:
        if material.mass < THRESHOLD:
            alert.append(material)

    return alert # return an array of materials with mass below 50g

async def job_complete_listener(mapper, connection, target):
    """
    A function triggered by the listener when the Material table is updated.  It checks for materials below the threshold value.

    Args: 
        mapper (object): SQLAlchemy mapper associated with the Material class.
        connection (object): the database connection object.
        target (Material): the target Material instance that was updated in the database.

    Returns:
        A list of materials that have a mass below the threshold value to websocket connection with UID 'low_stock'.
    """    
    session = SessionLocal()    # Create a new session instance for interacting with the database
    
    # Create a MaterialRepository instance to get a list of all materials
    repo = MaterialRepository(session)
    materials = repo.get_all_materials()

    # Retrieve all materials with a mass below the threshold
    alert_materials = await quantity_poll(materials)
    
    session.close() # Close the session once we are done
    
    # Send the alert materials to all active WebSocket connections
    if alert_materials:
        user_id = 'low_stock'
        alert_data = {
            'message': 'Low-stock materials alert!',
            'materials': [material.dict() for material in alert_materials]
        }
        # Send alert to the specific user
        await ws_manager.send_personal_message(user_id, alert_data)

    #return alert_materials  # Return the array of materials with a mass below the threshold