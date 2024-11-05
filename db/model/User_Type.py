import sqlite3

class User_Type:
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

            data = "UPDATE user_type SET type_name = '"+newName+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new type name for User class successful.")
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting type name data from User Type class", e)
        
        finally:
            if (conn):
                conn.close()
                print("Connection from User Type class closed.")

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

            data = "SELECT * FROM user_type" # Select all from the user_type table
            cursor.execute(data)        # Set the cursor to execute this instruction
            rows = cursor.fetchall()    # Fetch all the rows from the user_type table

            for x in rows:  # For each row, append the element to the result array
                result.append(x)

            # Return the result array after closing the connection
            conn.close()

        except sqlite3.Error as e:
            print("Error while getting all data from User Type class", e)
        
        finally:
            if (conn):
                conn.close()
                print("Connection from User Type class closed.")

        return result