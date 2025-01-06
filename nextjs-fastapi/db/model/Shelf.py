from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship
from .base import Base  # Import Base from a separate file


class Shelf(Base):
    # Constructor

    __tablename__ = 'shelfs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    humidity_pct = Column(Float, nullable=False)
    temperature_cel = Column(Float, nullable=False)

    #Relationships
    materials = relationship("Material", backref="shelf", cascade='all, delete')

    def __repr__(self):
        return f"<Shelf(id={self.id}, humidity_pct={self.humidity_pct}, temperature_cel={self.temperature_cel})>"

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of Shelf stored in the shelf table.
        """
        return session.query(cls).all()