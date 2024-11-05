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
        

    def setHPass(self, newHashedPassword):
        """
        Sets the Hashed Password of the current instance of user.
        """
        self.hashed_password = newHashedPassword
        # Call DB

    def setEmail(self, newEmail):
        """
        Sets the email address of the current instance of user.
        """
        self.email = newEmail
        # Call DB
    
    def setUserTypeID(self, newUTID):
        """
        Sets the user type ID of the current instance of user.
        """
        self.user_type_id = newUTID
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

        data = "SELECT * FROM user" # Select all from the user table
        cursor.execute(data)        # Set the cursor to execute this instruction
        rows = cursor.fetchall()    # Fetch all the rows from the user table

        for x in rows:  # For each row, append the element to the result array
            result.append(x)

        # Return the result array after closing the connection
        conn.close()
        return result