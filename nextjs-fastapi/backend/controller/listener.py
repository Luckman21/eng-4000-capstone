from db.repositories.MaterialRepository import MaterialRepository
from backend.controller import constants
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

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
    session = SessionLocal()    # Create a new session instance for interacting with the database
    
    # Create a MaterialRepository instance to get a list of all materials
    repo = MaterialRepository(session)
    materials = repo.get_all_materials()

    # Retrieve all materials with a mass below the threshold
    alert_materials = await quantity_poll(materials)
    
    session.close() # Close the session once we are done

    # DEBUG PRINT STATEMENT REMOVE FROM FINAL VERSION
    # Print the names (colours) of the materials returned
    print("\n\n\nMATERIALS BELOW THRESHOLD VALUE!!!!")
    material_names = [material.colour for material in alert_materials]
    print(f"{material_names}")

    print("\n\n\n")
    return alert_materials  # Return the array of materials with a mass below the threshold