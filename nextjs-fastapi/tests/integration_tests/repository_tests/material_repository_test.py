import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.Material import Material
from db.model.MaterialType import MaterialType
from db.model.base import Base
from db.repositories.MaterialRepository import MaterialRepository
from db.repositories.MaterialTypeRepository import MaterialTypeRepository

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

    db_count = session.query(Material).count()

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
        assert db_count == session.query(Material).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()


def test_get_material_by_id(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    material = session.query(Material).filter_by(name="Dummy Material").first()

    repository = MaterialRepository(session)

    queried_material = repository.get_material_by_id(material.id)

    assert material.id == queried_material.id


def test_create_material(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialRepository(session)
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    material = repository.create_material("blue", "Dummy2", 2.4, material_type.id)
    queried_material = repository.get_material_by_id(material.id)

    assert queried_material is not None
    assert queried_material.mass == material.mass

    # Destroy
    session.query(Material).filter_by(name="Dummy2").delete()
    session.commit()


def test_update_material(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialRepository(session)
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    # Fetch an existing material and update its data
    material = repository.create_material("blue", "Dummy2", 2.4, material_type.id)

    queried_material = repository.get_material_by_id(material.id)

    assert queried_material.colour == "blue"

    repository.update_material(material, colour="grey")

    new_queried_material = repository.get_material_by_id(material.id)

    assert new_queried_material.colour == "grey"

    # Destroy
    session.query(Material).filter_by(name="Dummy2").delete()
    session.commit()

def test_delete_material(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialRepository(session)
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    # Fetch an existing material and update its data
    material = repository.create_material("blue", "Dummy2", 2.4, material_type.id)

    queried_material = repository.get_material_by_id(material.id)

    assert queried_material is not None

    repository.delete_material(material)

    queried_material = repository.get_material_by_id(material.id)

    assert queried_material is None

