from sqlalchemy import create_engine, Column, Integer, String, Float, CheckConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from .base import Base  # Import Base from a separate file

# Base class for SQLAlchemy (this is the table essentially)


class Material(Base):
    __tablename__ = 'materials'

    # Attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    colour = Column(String, nullable=False)
    supplier_link = Column(String, nullable=False)
    mass = Column(Float, nullable=False)

    # Foreign Key
    material_type_id = Column(Integer, ForeignKey('material_types.id'), nullable=False)
    shelf_id = Column(Integer, ForeignKey('shelfs.id'), nullable=False)

    # Enforce the CHECK constraint (mass >= 0)
    __table_args__ = (
        CheckConstraint('mass >= 0', name='check_mass_non_negative'),
    )

    material_type = relationship("MaterialType", backref="materials")
    shelf_type = relationship("Shelf", backref="materials")

    # Set Methods
    def setColour(self, newColour):
        if type(newColour) is not str:
            raise ValueError("colour must be string")
        self.colour = newColour

    def setSupplierLink(self, new_link):
        if type(new_link) is not str:
            raise ValueError("link must be string")
        self.supplier_link = new_link

    def setMaterialTypeID(self, type):
        if isinstance(type, int):  # If an ID is provided
            try:
                self.material_type_id = type  # Set the related MaterialType object
            except Exception:
                raise ValueError(f"MaterialType with ID {type} does not exist.")
        else:
            raise ValueError("The 'type' must be either an integer (ID) or a MaterialType object.")

    def setShelfID(self, shelf_id):
        if not isinstance(shelf_id, int):
            raise ValueError("Shelf ID must be an integer.")
        self.shelf_id = shelf_id

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of Material stored in the Material table.
        """
        return session.query(cls).all()