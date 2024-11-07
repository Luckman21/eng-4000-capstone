import sqlite3
from sqlalchemy import Column, Integer, Float
from .base import Base  # Import Base from a separate file


class Shelf(Base):
    # Constructor

    __tablename__ = 'shelf'

    id = Column(Integer, primary_key=True, autoincrement=True)
    humidity_pct = Column(Float, nullable=False)
    temperature_cel = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Shelf(id={self.id}, humidity_pct={self.humidity_pct}, temperature_cel={self.temperature_cel})>"

    
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

            data = "SELECT * FROM shelf" # Select all from the shelf table
            cursor.execute(data)        # Set the cursor to execute this instruction
            rows = cursor.fetchall()    # Fetch all the rows from the shelf table

            for x in rows:  # For each row, append the element to the result array
                result.append(x)

            # Return the result array after closing the connection
            conn.close()
        
        except sqlite3.Error as e:
            print("Error while getting all data from Shelf class", e)
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Shelf class closed.")

        return result