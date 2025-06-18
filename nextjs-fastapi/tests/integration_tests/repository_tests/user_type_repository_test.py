import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.UserType import UserType
from db.model.base import Base
from db.repositories.UserTypeRepository import UserTypeRepository
from backend.controller import constants


@pytest.fixture(scope='module')
def setup_database(request):
    engine = create_engine(constants.DATABASE_URL, echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    db_count = session.query(UserType).count()

    # Add some dummy data
    dummy_user_type = UserType(type_name="Plastic")
    session.add(dummy_user_type)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(UserType).filter_by(type_name="Plastic").delete()
        session.commit()
        assert db_count == session.query(UserType).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session
    session.close()


def test_get_user_type_by_id(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    user_type = session.query(UserType).filter_by(type_name="Plastic").first()

    repository = UserTypeRepository(session)

    queried_user_type = repository.get_user_type_by_id(user_type.id)

    assert user_type.id == queried_user_type.id


def test_create_user_type(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = UserTypeRepository(session)

    user_type = repository.create_user_type("dummy")
    queried_user_type = repository.get_user_type_by_id(user_type.id)

    assert queried_user_type is not None

    # Destroy
    session.query(UserType).filter_by(type_name="dummy").delete()
    session.commit()


def test_update_user_type(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = UserTypeRepository(session)

    user_type = repository.create_user_type("dummy")
    queried_user_type = repository.get_user_type_by_id(user_type.id)

    repository.update_user_type(queried_user_type, "dummy1")

    queried_user_type = repository.get_user_type_by_id(user_type.id)

    assert queried_user_type.type_name == "dummy1"

    # Destroy
    session.query(UserType).filter_by(type_name="dummy1").delete()
    session.commit()


def test_delete_material_type(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = UserTypeRepository(session)

    user_type = repository.create_user_type("dummy")
    queried_user_type = repository.get_user_type_by_id(user_type.id)

    assert queried_user_type is not None

    repository.delete_user_type(queried_user_type)

    queried_user_type = repository.get_user_type_by_id(user_type.id)

    assert queried_user_type is None

