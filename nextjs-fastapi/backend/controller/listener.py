import asyncio
import json
from db.repositories.MaterialRepository import MaterialRepository
from db.repositories.ShelfRepository import ShelfRepository
from backend.controller import constants
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from backend.controller.manager import manager

# Create an engine and local session for connection to the database
engine = create_engine(constants.DATABASE_URL, echo=True)
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
    alert = []  # create an array for materials with a mass below 50g

    # Iterate through all materials, append those with a mass below the threshold value
    for material in materials:
        if material.mass < constants.THRESHOLD:
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




async def low_shelf_reader(shelfs):
    alert = []  
    for shelf in shelfs:
        if shelf.humidity_pct > 20 or shelf.temperature_cel > 30:
            alert.append(shelf)
    return alert



async def shelf_update_listener(mapper, connection, target):
    session = SessionLocal()
    repo = ShelfRepository(session)
    alert_shelfs = await low_shelf_reader(repo.get_all_shelves())
    session.close()

   
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

        # Wait until WebSocket is ready before sending
        
        await manager.send_alerts(json_data)
