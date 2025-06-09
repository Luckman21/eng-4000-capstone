import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.MaterialType import MaterialType
from db.model.base import Base
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from backend.controller import constants



@pytest.fixture(scope='module')
def setup_database(request):
    engine = create_engine(constants.DATABASE_URL, echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    db_count = session.query(MaterialType).count()

    # Add some dummy data
    dummy_material_type = MaterialType(type_name="Plastic")
    session.add(dummy_material_type)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(MaterialType).filter_by(type_name="Plastic").delete()
        session.commit()
        assert db_count == session.query(MaterialType).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session
    session.close()


def test_get_material_type_by_id(setup_database):
    session = setup_database
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    repository = MaterialTypeRepository(session)

    queried_material_type = repository.get_material_type_by_id(material_type.id)

    assert material_type.id == queried_material_type.id


def test_create_material(setup_database):
    session = setup_database
    repository = MaterialTypeRepository(session)

    material_type = repository.create_material_type("dummy")
    queried_material_type = repository.get_material_type_by_id(material_type.id)

    assert queried_material_type is not None

    # Destroy
    session.query(MaterialType).filter_by(type_name="dummy").delete()
    session.commit()


def test_update_material_type(setup_database):
    session = setup_database
    repository = MaterialTypeRepository(session)

    material_type = repository.create_material_type("dummy")
    queried_material_type = repository.get_material_type_by_id(material_type.id)

    repository.update_material_type(queried_material_type, "dummy1")

    queried_material_type = repository.get_material_type_by_id(material_type.id)

    assert queried_material_type.type_name == "dummy1"

    # Destroy
    session.query(MaterialType).filter_by(type_name="dummy1").delete()
    session.commit()


def test_delete_material_type(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialTypeRepository(session)

    material_type = repository.create_material_type("dummy")
    queried_material_type = repository.get_material_type_by_id(material_type.id)

    assert queried_material_type is not None

    repository.delete_material_type(queried_material_type)

    queried_material_type = repository.get_material_type_by_id(material_type.id)

    assert queried_material_type is None


def test_material_type_existance(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = MaterialTypeRepository(session)
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    assert material_type is not None

    assert repository.type_exists(material_type.id) is True

    queried_material_type = repository.get_material_type_by_id(-1)

    assert queried_material_type is None

    assert repository.type_exists(-1) is not True

    # Destroy
    session.query(MaterialType).filter_by(type_name="Plastic").delete()
    session.commit()

