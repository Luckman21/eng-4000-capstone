import sqlite3
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .User_Type import UserType  # Import UserType from user_type.py
from .base import Base  # Import Base from a separate file

class User(Base):

    # Constructor
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False) # HASHED
    email = Column(String, nullable=False, unique=True)

    user_type_id = Column(Integer, ForeignKey('user_type.id'))

    user_type = relationship('UserType', backref='users', cascade='all, delete')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

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