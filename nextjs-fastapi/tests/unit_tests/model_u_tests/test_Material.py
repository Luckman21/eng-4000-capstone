import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.Material import Material
from db.model.MaterialType import MaterialType
from db.model.base import Base

# Use an existing database instead of an in-memory one
@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = 'sqlite:///nextjs-fastapi/db/capstone_db.db'
    engine = create_engine(DATABASE_URL, echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add some dummy data
    dummy_material_type = MaterialType(type_name="Plastic")
    session.add(dummy_material_type)
    session.commit()

    dummy_material = Material(
        name="Dummy Material",
        colour="Red",
        mass=10.5,
        material_type_id=dummy_material_type.id
    )
    session.add(dummy_material)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(Material).filter_by(name="Dummy Material").delete()
        session.query(MaterialType).filter_by(type_name="Plastic").delete()
        session.commit()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()

# Example test case 1: Test adding and removing dummy data
def test_add_dummy_material(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Verify that the dummy data is inserted
    inserted_material = session.query(Material).filter_by(name="Dummy Material").first()
    assert inserted_material is not None
    assert inserted_material.colour == "Red"

    queried_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    assert inserted_material.material_type_id == queried_type.id

    # The dummy data will be rolled back after the test

# Example test case 4: Test a material update
def test_update_material_colour(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    material_to_update = session.query(Material).filter_by(name="Dummy Material").first()
    assert material_to_update is not None

    material_to_update.setColour("Dark Gray")
    session.commit()

    # Verify that the material was updated
    updated_material = session.query(Material).filter_by(name="Dummy Material").first()
    assert updated_material.colour == "Dark Gray"

    # Rollback happens after this test so the data will be reverted

# Example test case 4: Test a material update
def test_update_material_name(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    material_to_update = session.query(Material).filter_by(name="Dummy Material").first()
    assert material_to_update is not None

    material_to_update.setName("Cookies")
    session.commit()

    # Verify that the material was updated
    updated_material = session.query(Material).filter_by(name="Cookies").first()
    assert updated_material.name == "Cookies"

    # Rollback happens after this test so the data will be reverted