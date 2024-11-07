import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .Material_Type import MaterialType
from .base import Base  # Import Base from a separate file

# Base class for SQLAlchemy (this is the table essentially)


class Material(Base):
    __tablename__ = 'materials'

    # Attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    colour = Column(String, nullable=False)
    name = Column(String, nullable=False)
    mass = Column(Float, nullable=False)

    # Foreign Key
    material_type_id = Column(Integer, ForeignKey('material_types.id'), nullable=False)

    # Enforce the CHECK constraint (mass >= 0)
    __table_args__ = (
        CheckConstraint('mass >= 0', name='check_mass_non_negative'),
    )

    material_type = relationship("MaterialType", backref="materials", cascade='all, delete')


    def __init__(self, db_url='sqllite:///capstone_db.db'):
        self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        base.metadata.create_all(self.engine) # Create tables if not exist

    # Set Methods

    def setColour(self, newColour):
        self.colour = newColour
        
        # Update colour in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE material SET colour = '"+newColour+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new colour for Material class successful.")  # TODO: Remove print statement before deployment
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting colour data from Material class", e) # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Material class closed.") # TODO: Remove print statement before deployment

    def setName(self, newName):
        self.name = newName

        # Update name in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE material SET name = '"+newName+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new name for Material class successful.")    # TODO: Remove print statement before deployment
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting name data from Material class", e)   # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Material class closed.") # TODO: Remove print statement before deployment

    def setMaterialTypeID(self, newMTID):
        self.material_type_id = newMTID

        # Update Material Type ID in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE material SET material_type_id = '"+newMTID+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new Material Type ID for Material class successful.")
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting Material Type ID data from Material class", e)
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Material class closed.")

    # For reference on this part https://youtu.be/fKXhuOvjQQ8?si=-KNLP-ykp-mbCfJ2
    def getAll():
        """
        Returns all the instances of User stored in the user table.
        """
        result = [] # An array to store all the results

        try:
            # Connect to the database (it will create the file if it doesn't exist)
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "SELECT * FROM material" # Select all from the material table
            cursor.execute(data)        # Set the cursor to execute this instruction
            rows = cursor.fetchall()    # Fetch all the rows from the material table

            for x in rows:  # For each row, append the element to the result array
                result.append(x)

            # Return the result array after closing the connection
            conn.close()

        except sqlite3.Error as e:
            print("Error while getting all data from Material class", e)    # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Material class closed.") # TODO: Remove print statement before deployment

        return result