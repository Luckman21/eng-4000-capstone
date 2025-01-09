from sqlalchemy import Column, Integer, Float, CheckConstraint
from .base import Base  # Import Base from a separate file


class Shelf(Base):
    # Constructor

    __tablename__ = 'shelfs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    humidity_pct = Column(Float, nullable=False)
    temperature_cel = Column(Float, nullable=False)

    # Enforce the CHECK constraint (mass >= 0)
    __table_args__ = (
        CheckConstraint('humidity_pct >= 0', name='check_humidity_non_negative'),
        CheckConstraint('temperature_cel >= -273.15', name='check_temp_below_possible'),
        CheckConstraint('temperature_cel <= 1000', name='check_temp_too_high'),
    )

    def __repr__(self):
        return f"<Shelf(id={self.id}, humidity_pct={self.humidity_pct}, temperature_cel={self.temperature_cel})>"

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of Shelf stored in the shelf table.
        """
        return session.query(cls).all()