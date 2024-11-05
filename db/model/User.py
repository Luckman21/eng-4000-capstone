import sqlite3

class User:
    # Constructor
    def __init__(self, id, username, hashed_password, email, user_type_id):
        """
        Constructor for the User class.
        """
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
        self.user_type_id = user_type_id

    # Set Methods

    def setUsername(self, newUsername):
        """
        Sets the username of the current instance of user.
        """
        self.username = newUsername

        # Update name in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE user SET username = '"+newUsername+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new username for User class successful.")    # TODO: Remove print statement before deployment
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting username data from User class", e)   # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from User class closed.") # TODO: Remove print statement before deployment
        

    def setHPass(self, newHashedPassword):
        """
        Sets the Hashed Password of the current instance of user.
        """
        self.hashed_password = newHashedPassword

        # Update hashed password in the database based on ID
        # Update name in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE user SET password = '"+newHashedPassword+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new password for User class successful.")    # TODO: Remove print statement before deployment
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting password data from User class", e)   # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from User class closed.") # TODO: Remove print statement before deployment

    def setEmail(self, newEmail):
        """
        Sets the email address of the current instance of user.
        """
        self.email = newEmail
        
        # Update email in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE user SET email = '"+newEmail+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new email address for User class successful.")   # TODO: Remove print statement before deployment
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting email address data from User class", e)  # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from User class closed.") # TODO: Remove print statement before deployment
    
    def setUserTypeID(self, newUTID):
        """
        Sets the user type ID of the current instance of user.
        """
        self.user_type_id = newUTID

        # Update user type ID in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE user SET user_type_id = '"+newUTID+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new user_type_id for User class successful.")    # TODO: Remove print statement before deployment
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting user_type_id data from User class", e)   # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from User class closed.") # TODO: Remove print statement before deployment

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

            data = "SELECT * FROM user" # Select all from the user table
            cursor.execute(data)        # Set the cursor to execute this instruction
            rows = cursor.fetchall()    # Fetch all the rows from the user table

            for x in rows:  # For each row, append the element to the result array
                result.append(x)

            # Return the result array after closing the connection
            conn.close()

        except sqlite3.Error as e:
            print("Error while getting all data from User class", e)    # TODO: Remove print statement before deployment
        
        finally:
            if (conn):
                conn.close()
                print("Connection from User class closed.") # TODO: Remove print statement before deployment

        return result