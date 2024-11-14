from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .base import Base  # Import Base from a separate file



class MaterialType(Base):

    __tablename__ = 'material_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<MaterialType(id={self.id}, type_name={self.type_name})>"


    # Set Methods

    def setName(self, newName):
        if type(newName) is not str:
            raise ValueError("name must be string")
        self.name = newName

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of Material Type stored in table.
        """
        return session.query(cls).all()