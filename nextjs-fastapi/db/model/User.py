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

        if type(newUsername) is not str:
            raise ValueError("Username must be string")
        self.username = newUsername

    def setHPass(self, newHashedPassword):
        """
        Sets the Hashed Password of the current instance of user.
        """

        # Update hashed password in the database based on ID
        # Update name in the databsae based on the ID
        if type(newHashedPassword) is not str:
            raise ValueError("Password must be string")
        self.password = newHashedPassword


    def setEmail(self, newEmail):
        """
        Sets the email address of the current instance of user.
        """

        if type(newEmail) is not str:
            raise ValueError("Email must be string")
        self.email = newEmail
    
    def setUserTypeID(self, type):
        """
        Sets the user type ID of the current instance of user.
        """

        if isinstance(type, UserType):
            self.user_type = type
            self.user_type_id = type.id
        else:
            raise ValueError("Type can only be of UserType for Users")

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of User stored in the user table.
        """
        return session.query(cls).all()