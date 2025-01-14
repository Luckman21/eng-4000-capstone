from sqlalchemy import create_engine, Column, Integer, String, Float, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from .base import Base  # Import Base from a separate file
from .MaterialType import MaterialType

# Base class for SQLAlchemy (this is the table essentially)


class Material(Base):
    __tablename__ = 'materials'

    # Attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    colour = Column(String, nullable=False)
    name = Column(String, nullable=False)
    mass = Column(Float, nullable=False)

    # Foreign Key
    material_type_id = Column(Integer, ForeignKey('material_types.id'), nullable=False)

    # Enforce the CHECK constraint (mass >= 0)
    __table_args__ = (
        CheckConstraint('mass >= 0', name='check_mass_non_negative'),
    )

    material_type = relationship("MaterialType", backref="materials", cascade='all, delete')

    # Set Methods

    def setColour(self, newColour):
        if type(newColour) is not str:
            raise ValueError("colour must be string")
        self.colour = newColour

    def setName(self, newName):
        if type(newName) is not str:
            raise ValueError("name must be string")
        self.name = newName

    def setMaterialTypeID(self, type):

        if isinstance(type, int):  # If an ID is provided
            try:
                self.material_type_id = type  # Set the related MaterialType object
            except Exception:
                raise ValueError(f"MaterialType with ID {type} does not exist.")
        else:
            raise ValueError("The 'type' must be either an integer (ID) or a MaterialType object.")

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of Material stored in the Material table.
        """
        return session.query(cls).all()