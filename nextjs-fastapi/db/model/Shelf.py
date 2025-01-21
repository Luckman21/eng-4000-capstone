from sqlalchemy import Column, Integer, Float, CheckConstraint
from .base import Base  # Import Base from a separate file

class Shelf(Base):
    __tablename__ = 'shelfs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    humidity_pct = Column(Float, nullable=False)
    temperature_cel = Column(Float, nullable=False)

    # Enforce the CHECK constraint (humidity_pct >= 0, temperature_cel >= 0 && temperature_cel <= 50)
    __table_args__ = (
        CheckConstraint('humidity_pct >= 15', name='check_humidity_below_possible'),    # Minimum humidity recoreded by DHT11 sensor + Error
        CheckConstraint('humidity_pct <= 85', name='check_humidity_above_possible'),    # Maximum humidity recoreded by DHT11 sensor + Error
        CheckConstraint('temperature_cel >= -2', name='check_temp_below_possible'),     # Minimum temp recoreded by DHT11 sensor + Error
        CheckConstraint('temperature_cel <= 52', name='check_temp_above_possible'),     # Maximum temp recoreded by DHT11 sensor + Error  
    )

    def __repr__(self):
        return f"<Shelf(id={self.id}, humidity_pct={self.humidity_pct}, temperature_cel={self.temperature_cel})>"

    def __init__(self, humidity_pct, temperature_cel):
        # Type check for humidity_pct
        if not isinstance(humidity_pct, float):
            raise TypeError(f"humidity_pct must be a float, got {type(humidity_pct)}")
        
        # Type check for temperature_cel
        if not isinstance(temperature_cel, float):
            raise TypeError(f"temperature_cel must be a float, got {type(temperature_cel)}")
        
        # If the type checks pass, set the attributes
        self.humidity_pct = humidity_pct
        self.temperature_cel = temperature_cel

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of Shelf stored in the shelf table.
        """
        return session.query(cls).all()