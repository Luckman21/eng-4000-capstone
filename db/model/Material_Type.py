import sqlite3

class Material_Type:
    # Constructor

    def __init__(self, id, name):
        self.id = id
        self.name = name

    # Set Methods

    def setName(self, newName):
        self.name = newName

        # Update type name in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE material_type SET type_name = '"+newName+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new type name for Material Type class successful.")  # TODO: Remove print statement before deployment
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting type name data from Material Type class", e) # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Material Type class closed.")    # TODO: Remove print statement before deployment

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

            data = "SELECT * FROM material_type" # Select all from the material table
            cursor.execute(data)        # Set the cursor to execute this instruction
            rows = cursor.fetchall()    # Fetch all the rows from the material table

            for x in rows:  # For each row, append the element to the result array
                result.append(x)

            # Return the result array after closing the connection
            conn.close()
        
        except sqlite3.Error as e:
            print("Error while getting all data from Material Type class", e)   # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Material Type class closed.")    # TODO: Remove print statement before deployment

        return result