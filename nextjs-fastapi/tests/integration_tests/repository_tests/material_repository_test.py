import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.Material import Material
from db.model.MaterialType import MaterialType
from db.model.Shelf import Shelf
from db.model.base import Base
from db.repositories.MaterialRepository import MaterialRepository
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from backend.controller import constants
from sqlalchemy import text

# Use an existing database instead of an in-memory one
@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = "postgresql://postgres:0000@localhost/"

    # Create a unique temporary database for the test
    test_db_name = "capstone_test_db"
    engine = create_engine(DATABASE_URL)  # Connect to Postgres
    connection = engine.connect()

    # Use the connection in autocommit mode for non-transactional commands like CREATE DATABASE
    connection.execution_options(autocommit=True)

    # Create the database
    connection.execute(text(f"CREATE DATABASE {test_db_name}"))

    # Close the connection after creating the DB
    connection.close()

    # Now connect to the new database and create tables
    test_db_url = f"postgresql://postgres:0000@localhost/{test_db_name}"
    test_engine = create_engine(test_db_url)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(test_engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=test_engine)
    session = Session()

    db_count = session.query(Material).count()

    # Add some dummy data
    dummy_material_type = MaterialType(type_name="Plastic")
    session.add(dummy_material_type)
    session.commit()

    dummy_material = Material(
        supplier_link="Dummy Material",
        colour="Red",
        mass=10.5,
        material_type_id=dummy_material_type.id,
        shelf_id=1
    )
    session.add(dummy_material)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(Material).filter_by(supplier_link="Dummy Material").delete()
        session.query(MaterialType).filter_by(type_name="Plastic").delete()
        session.commit()
        assert db_count == session.query(Material).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()
    test_engine.dispose()  # Disconnect from test DB

    connection = engine.connect()
    connection.execution_options(autocommit=True)
    connection.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
    connection.close()  # Close the connection to finalize the drop


def test_get_material_by_id(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    material = session.query(Material).filter_by(supplier_link="Dummy Material").first()

    repository = MaterialRepository(session)

    queried_material = repository.get_material_by_id(material.id)

    assert material.id == queried_material.id


def test_create_material(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialRepository(session)
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    new_shelf = Shelf(humidity_pct=60.0, temperature_cel=25.0)
    session.add(new_shelf)
    session.commit()

    material = repository.create_material("blue", "Dummy2", 2.4, material_type.id, shelf_id=new_shelf.id)
    queried_material = repository.get_material_by_id(material.id)

    assert queried_material is not None
    assert queried_material.mass == material.mass
    assert queried_material.shelf_id == new_shelf.id

    # Destroy
    session.query(Material).filter_by(supplier_link="Dummy2").delete()
    session.commit()


def test_update_material(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialRepository(session)
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    new_shelf = Shelf(humidity_pct=60.0, temperature_cel=25.0)
    session.add(new_shelf)
    session.commit()

    # Fetch an existing material and update its data
    material = repository.create_material("blue", "Dummy2", 2.4, material_type.id, shelf_id=new_shelf.id)

    queried_material = repository.get_material_by_id(material.id)

    assert queried_material.colour == "blue"
    assert queried_material.shelf_id == new_shelf.id

    repository.update_material(material, colour="grey")

    new_queried_material = repository.get_material_by_id(material.id)

    assert new_queried_material.colour == "grey"

    repository.update_material(material, material_type_id=1)

    new_queried_material = repository.get_material_by_id(material.id)

    assert new_queried_material.material_type_id == 1

    # Destroy
    session.query(Material).filter_by(supplier_link="Dummy2").delete()
    session.query(Shelf).filter_by(id=new_shelf.id).delete()
    session.commit()


def test_material_existance(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialRepository(session)
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    # Fetch an existing material and update its data
    material = repository.create_material("blue", "Dummy2", 2.4, material_type.id, 1)

    queried_material = repository.get_material_by_id(material.id)

    assert queried_material is not None

    assert repository.material_exists(queried_material.id) is True

    queried_material = repository.get_material_by_id(-1)

    assert queried_material is None

    assert repository.material_exists(-1) is not True

    # Destroy
    session.query(Material).filter_by(supplier_link="Dummy2").delete()
    session.commit()


def test_delete_material(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialRepository(session)
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    new_shelf = Shelf(humidity_pct=60.0, temperature_cel=25.0)
    session.add(new_shelf)
    session.commit()

    # Fetch an existing material and update its data
    material = repository.create_material("blue", "Dummy2", 2.4, material_type.id, shelf_id=new_shelf.id)

    queried_material = repository.get_material_by_id(material.id)

    assert queried_material is not None

    repository.delete_material(material)

    queried_material = repository.get_material_by_id(material.id)

    assert queried_material is None

    session.query(Shelf).filter_by(id=new_shelf.id).delete()
    session.commit()


