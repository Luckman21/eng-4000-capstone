import sqlite3

class User_Type:
    # Constructor

    def __init__(self, id, name):
        self.id = id
        self.name = name

    # Set Methods

    def setName(self, newName):
        self.name = newName
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

        data = "SELECT * FROM user_type" # Select all from the user_type table
        cursor.execute(data)        # Set the cursor to execute this instruction
        rows = cursor.fetchall()    # Fetch all the rows from the user_type table

        for x in rows:  # For each row, append the element to the result array
            result.append(x)

        # Return the result array after closing the connection
        conn.close()
        return result