import sqlite3

class Shelf:
    # Constructor

    def __init__(self, id, humidity_pct, temperature_cel):
        self.id = id
        self.humidity_pct = humidity_pct
        self.temperature_cel = temperature_cel
    
    # Set Methods
    
    def setHumidityPCT(self, newHumidPCT):
        self.humidity_pct = newHumidPCT
        # Call DB
    
    def setTemperatureCel(self, newTempCel):
        self.temperature_cel = newTempCel
        # Call DB
    
    # For reference on this part https://youtu.be/fKXhuOvjQQ8?si=-KNLP-ykp-mbCfJ2
    def getAll():
        """
        Returns all the instances of User stored in the user table.
        """
        result = [] # An array to store all the results

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
        return result