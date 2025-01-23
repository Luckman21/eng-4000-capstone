import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.Shelf import Shelf
from db.model.base import Base
from db.repositories.ShelfRepository import ShelfRepository
from backend.controller import constants

# Use an existing database instead of an in-memory one
@pytest.fixture(scope='module')
def setup_database(request):
    engine = create_engine('sqlite:///:memory:', echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    db_count = session.query(Shelf).count()


    dummy_shelf = Shelf(
        humidity_pct = 50.0,
        temperature_cel = 30.0
    )
    session.add(dummy_shelf)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(Shelf).filter_by(humidity_pct=50.0, temperature_cel = 30.0).delete()
        session.commit()
        assert db_count == session.query(Shelf).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()


def test_get_shelf_by_id(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    shelf = session.query(Shelf).filter_by(humidity_pct=50.0, temperature_cel = 30.0).first()

    repository = ShelfRepository(session)

    queried_shelf = repository.get_shelf_by_id(shelf.id)

    assert shelf.id == queried_shelf.id


def test_create_shelf(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = ShelfRepository(session)

    shelf = repository.create_shelf(30.0, 30.0)
    queried_shelf = repository.get_shelf_by_id(shelf.id)

    assert queried_shelf is not None
    assert queried_shelf.humidity_pct == shelf.humidity_pct

    # Destroy
    session.query(Shelf).filter_by(humidity_pct=30.0, temperature_cel = 30.0).delete()
    session.commit()


def test_update_shelf(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = ShelfRepository(session)

    # Fetch an existing material and update its data
    shelf = repository.create_shelf(40.0, 40.0)

    queried_shelf = repository.get_shelf_by_id(shelf.id)

    assert queried_shelf.humidity_pct == 40.0
    assert queried_shelf.temperature_cel == 40.0

    repository.update_shelf(shelf, new_temperature_cel = 50.0)

    new_queried_shelf = repository.get_shelf_by_id(shelf.id)

    assert new_queried_shelf.temperature_cel == 50.0


    # Destroy
    session.query(Shelf).filter_by(humidity_pct=40.0, temperature_cel=50.0).delete()
    session.commit()


def test_delete_shef(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = ShelfRepository(session)

    # Fetch an existing shelf and update its data
    shelf = repository.create_shelf(40.0, 40.0)

    queried_shelf = repository.get_shelf_by_id(shelf.id)

    assert queried_shelf is not None

    repository.delete_shelf(shelf)

    queried_shelf = repository.get_shelf_by_id(shelf.id)

    assert queried_shelf is None


