import sqlite3

class Material:
    # Constructor

    def __init__(self, id, colour, name, material_type_id):
        self.id = id
        self.colour = colour
        self.name = name
        self.material_type_id = material_type_id

    # Set Methods

    def setColour(self, newColour):
        self.colour = newColour
        # Call DB

    def setName(self, newName):
        self.name = newName
        # Call DB

    def setMaterialTypeID(self, newMTID):
        self.material_type_id = newMTID
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

        data = "SELECT * FROM material" # Select all from the material table
        cursor.execute(data)        # Set the cursor to execute this instruction
        rows = cursor.fetchall()    # Fetch all the rows from the material table

        for x in rows:  # For each row, append the element to the result array
            result.append(x)

        # Return the result array after closing the connection
        conn.close()
        return result