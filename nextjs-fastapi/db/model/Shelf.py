import sqlite3
from sqlalchemy import Column, Integer, Float
from .base import Base  # Import Base from a separate file


class Shelf(Base):
    # Constructor

    __tablename__ = 'shelf'

    id = Column(Integer, primary_key=True, autoincrement=True)
    humidity_pct = Column(Float, nullable=False)
    temperature_cel = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Shelf(id={self.id}, humidity_pct={self.humidity_pct}, temperature_cel={self.temperature_cel})>"

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of Shelf stored in the shelf table.
        """
        return session.query(cls).all()