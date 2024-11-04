import sqlite3

class User:
    # Constructor
    def __init__(self, id, username, hashed_password, email, user_type_id):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
        self.user_type_id = user_type_id

    # Set Methods

    def setID(self, newID):
        self.id = newID
        # Call DB

    def setUsername(self, newUsername):
        self.username = newUsername
        # Call DB

    def setHPass(self, newHashedPassword):
        self.hashed_password = newHashedPassword
        # Call DB

    def setEmail(self, newEmail):
        self.email = newEmail
        # Call DB
    
    def setUserTypeID(self, newUTID):
        self.user_type_id = newUTID
        # Call DB

# TODO: update DB info, getAll Method

# Connect to the database (it will create the file if it doesn't exist)
#conn = sqlite3.connect('../capstone_db.db') # TODO: check if this is the correct DB to connect to
#cursor = conn.cursor()
#conn.close()