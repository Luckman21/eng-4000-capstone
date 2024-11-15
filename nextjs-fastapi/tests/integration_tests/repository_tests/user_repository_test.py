import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.User import User
from db.model.UserType import UserType
from db.model.base import Base
from db.repositories.UserRepository import UserRepository
from db.repositories.UserTypeRepository import UserTypeRepository

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

    db_count = session.query(User).count()

    # Add some dummy data
    dummy_user_type = UserType(type_name="Cheese")
    session.add(dummy_user_type)
    session.commit()

    dummy_user = User(
        username="Tom Jones",
        password="cheese whiz",  # Assumes password is already hashed
        email="fake@google.ca",
        user_type_id= dummy_user_type.id
    )
    session.add(dummy_user)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(User).filter_by(name="Tom Jones").delete()
        session.query(UserType).filter_by(type_name="Cheese").delete()
        session.commit()
        assert db_count == session.query(User).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()


def test_get_user_by_id(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    user = session.query(User).filter_by(name="Tom Jones").first()

    repository = UserRepository(session)

    queried_user = repository.get_user_by_id(user.id)

    assert user.id == queried_user.id


def test_create_user(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = UserRepository(session)
    user_type = session.query(UserType).filter_by(type_name="Cheese").first()

    user = repository.create_material("James", "cheesewhiz", "fake@email.com", user_type.id)
    queried_user = repository.get_user_by_id(user.id)

    assert queried_user is not None


    # Destroy
    session.query(User).filter_by(name="James").delete()
    session.commit()


def test_update_material(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = UserRepository(session)
    user_type = session.query(UserType).filter_by(type_name="Cheese").first()

    # Fetch an existing material and update its data
    user = repository.create_material("James", "cheesewhiz", "fake@email.com", user_type.id)

    queried_user = repository.get_user_by_id(user.id)

    assert queried_user.email == "fake@email.com"

    repository.update_material(user, email="fake@email.ca")

    new_queried_user = repository.get_user_by_id(user.id)

    assert new_queried_user.colour == "fake@email.ca"

    # Destroy
    session.query(User).filter_by(name="James").delete()
    session.commit()

def test_delete_material(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = UserRepository(session)
    user_type = session.query(UserType).filter_by(type_name="Cheese").first()

    # Fetch an existing material and update its data
    user = repository.create_material("James", "cheesewhiz", "fake@email.com", user_type.id)

    queried_user = repository.get_material_by_id(user.id)

    assert queried_user is not None

    repository.delete_material(user)

    queried_user = repository.get_material_by_id(user.id)

    assert queried_user is None

