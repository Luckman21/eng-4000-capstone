import asyncio
import json
from db.repositories.MaterialRepository import MaterialRepository
from db.repositories.ShelfRepository import ShelfRepository
from backend.controller import constants
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from backend.controller.manager import manager
from asyncio import get_running_loop
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from backend.service.mailer.LowStockMailer import LowStockMailer
from backend.service.mailer.EnviroWarningMailer import EnviroWarningMailer
from db.repositories.UserRepository import UserRepository

DATABASE_URL = constants.DATABASE_URL_ASYNC  # Example: "postgresql+asyncpg://user:password@localhost/dbname"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))



# A polling function to check the mass of each material in the table
async def quantity_poll(materials):
    """
    A polling function to check the mass of each material in the table, returns an array of materials with a mass below the threshold value.

    Args:
        materials(List[Material]): A list of Material objects to iterate through.

    Returns:
        List[Material]: A list of materials with a mass below the threshold value.
    """
    alerts = []  # create an array for materials with a mass below 50g
    superadmins = UserRepository(SessionLocal).get_all_superadmins()

    # Iterate through all materials, append those with a mass below the threshold value
    for material in materials:
        if material.mass < constants.THRESHOLD:
            alerts.append(material)
            
    for alert in alerts:
        for superadmin in superadmins:
            LowStockMailer(constants.MAILER_EMAIL).send_notification(superadmin.email, alert.product_type, alert.colour, alert.supplier_link)
    return alerts # return an array of materials with mass below 50g


async def job_complete_listener(mapper, connection, target):
    """
    A function triggered by the listener when the Material table is updated.  It checks for materials below the threshold value.

    Args: 
        mapper (object): SQLAlchemy mapper associated with the Material class.
        connection (object): the database connection object.
        target (Material): the target Material instance that was updated in the database.

    Returns:
        A list of materials that have a mass below the threshold value.
    """    
    session = SessionLocal()  # Create a new session to query the database
    print(f"🆔 Manager ID (listener): {id(manager)}")  # Ensure it's the same instance
    
    # Create a MaterialRepository instance to get a list of all materials
    repo = MaterialRepository(session)
    materials = repo.get_all_materials()

    # Retrieve all materials with a mass below the threshold
    alert_materials = await quantity_poll(materials)
    
    session.close() # Close the session once we are done

   
    data = {
        "type": "material_alert",
        "data": [
            {"id": m.id, "colour": m.colour, "mass": m.mass, "supplier_link": m.supplier_link} for m in alert_materials
        ] if alert_materials else []
    }      

    json_data = json.dumps(data)  # Convert to JSON string
    print(json_data)
    if json_data:
        # Fix: Ensure it runs inside the correct event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(manager.send_alerts(json_data))  # Safe in async
        else:
            asyncio.run(manager.send_alerts(json_data))  # Needed for sync calls
    return alert_materials 


async def shelf_update_listener(mapper, connection, target):
    try:
        async with AsyncSessionLocal() as session:  # Correctly manage session
            repo = ShelfRepository(session)
            user_repo = UserRepository(session)
            superadmins = await user_repo.get_all_superadmins_async()
            high_humidity_shelves = await repo.get_high_humidity_shelves_async()
            high_temp_shelves = await repo.get_high_temperature_shelves_async()
            for shelf in high_humidity_shelves:
                for superadmin in superadmins:
                    EnviroWarningMailer(constants.MAILER_EMAIL).send_notification(superadmin.email,"humidity" ,shelf.id)
            for shelf in high_temp_shelves:
                for superadmin in superadmins:
                    EnviroWarningMailer(constants.MAILER_EMAIL).send_notification(superadmin.email,"temperature" ,shelf.id)
            combined_shelves_dict = {}

            for shelf in high_humidity_shelves + high_temp_shelves:
                # Only keep one entry per shelf.id
                if shelf.id not in combined_shelves_dict:
                    combined_shelves_dict[shelf.id] = shelf

            # Final deduplicated list
            alert_shelfs = list(combined_shelves_dict.values())
    except Exception as e:
        print(f"Error while fetching shelves: {e}")
        return []

    print(f"🛑 Active WebSockets BEFORE sending shelf alert: {len(manager.active_connections)}")

    if alert_shelfs:
        data = {
            "type": "shelf_alert",
            "data": [
                {"id": s.id, "humidity": s.humidity_pct, "temperature": s.temperature_cel}
                for s in alert_shelfs
            ]
        }

        json_data = json.dumps(data)

        print(f"📤 Sending shelf alert: {json_data}")

        # Ensure we're scheduling the async task correctly depending on whether the loop is running
        try:

            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If the event loop is running, safely schedule the task
                asyncio.create_task(manager.send_alerts(json_data))
            else:
                # If no event loop is running, run the task directly using asyncio.run
                print("No event loop running, using run_coroutine_threadsafe.")
                asyncio.run_coroutine_threadsafe(manager.send_alerts(json_data), loop)
        except Exception as e:
            print(f"❌ Error while scheduling alert: {e}")