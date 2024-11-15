from sqlalchemy import Column, Integer, String
from .base import Base  # Import Base from a separate file


class UserType(Base):
    # Constructor

    __tablename__ = 'user_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<UserType(id={self.id}, type_name={self.type_name})>"


    # Set Methods

    def setName(self, newName):

        if type(newName) is not str:
            raise ValueError("name must be string")
        self.type_name = newName

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of User_Type stored in the user_type table.
        """
        return session.query(cls).all()