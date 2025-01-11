import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from db.model.Shelf import Shelf
from db.model.base import Base

# Fixture to setup an in-memory database for testing
@pytest.fixture(scope='module')
def session():
    # Setup the in-memory SQLite database engine
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # Create all tables defined in Base

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Cleanup after test
    session.close()
    engine.dispose()

# Test case for Shelf creation and initialization
def test_shelf_creation(session):
    # Create a valid Shelf
    shelf = Shelf(humidity_pct=60.5, temperature_cel=22.0)
    session.add(shelf)
    
    session.commit()

    # Test that the Shelf was successfully added
    assert shelf.id is not None
    assert shelf.humidity_pct == 60.5
    assert shelf.temperature_cel == 22.0

    # Rollback the session after the test
    session.rollback()

# Test invalid humidity_pct (negative value) raises IntegrityError
def test_shelf_invalid_humidity(session):
    shelf = Shelf(humidity_pct=-10.0, temperature_cel=22.0)  # Invalid humidity (negative value)
    session.add(shelf)

    # Check for IntegrityError due to negative humidity (if you want to enforce non-negative humidity)
    with pytest.raises(IntegrityError):
        session.commit()

    # Rollback the session after the test
    session.rollback()

# Test invalid temperature_cel (negative value) raises IntegrityError
def test_shelf_invalid_temperature(session):
    shelf = Shelf(humidity_pct=60.5, temperature_cel=-273.16)  # Invalid temperature (beyond minimum possible temperature in C)
    session.add(shelf)

    # Check for IntegrityError due to negative temperature (if you want to enforce non-negative temperature)
    with pytest.raises(IntegrityError):
        session.commit()

    # Rollback the session after the test
    session.rollback()

# Test getAll method for retrieving all shelves
def test_get_all_shelves(session):
    shelf1 = Shelf(humidity_pct=55.0, temperature_cel=20.0)
    shelf2 = Shelf(humidity_pct=60.0, temperature_cel=23.5)
    session.add(shelf1)
    session.add(shelf2)

    session.commit()

    # Test the getAll method to fetch all shelves
    shelves = Shelf.getAll(Shelf, session)
    assert len(shelves) == 3  # We added two shelves, plus the initial shelf from test 1
    assert shelves[0].humidity_pct == 60.5
    assert shelves[0].temperature_cel == 22.0
    assert shelves[1].humidity_pct == 55.0
    assert shelves[1].temperature_cel == 20.0
    assert shelves[2].humidity_pct == 60.0
    assert shelves[2].temperature_cel == 23.5

    # Rollback the session after the test
    session.rollback()

# Test invalid input types (humidity_pct or temperature_cel must be floats)
def test_invalid_input_types(session):
    with pytest.raises(TypeError):
        Shelf(humidity_pct='invalid', temperature_cel=22.0)  # Humidity should be float
    
    with pytest.raises(TypeError):
        Shelf(humidity_pct=60.5, temperature_cel='invalid')  # Temperature should be float

    # Rollback the session after the test
    session.rollback()