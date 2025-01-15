# tests/test_update_mass.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.User import User
from db.model.UserType import UserType
from db.model.base import Base
from db.repositories.MaterialRepository import MaterialRepository

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
    dummy_user_type = UserType(type_name="Plastic")
    session.add(dummy_user_type)
    session.commit()

    dummy_user = User(
        username="Dummy Material",
        email="red@email.com",
        password="123",
        user_type_id=dummy_user_type.id
    )
    session.add(dummy_user)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(User).filter_by(username="Dummy Material").delete()
        session.query(UserType).filter_by(type_name="Plastic").delete()
        session.commit()
        assert db_count == session.query(User).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()


# Initialize the TestClient to simulate schemas
client = TestClient(get_app())

def test_delete_user_success(setup_database):
    session = setup_database

    user = session.query(User).filter_by(username="Dummy Material").first()

    assert user is not None, "Dummy material should exist in the database"

    user_id = user.id

    # Send a PUT request with valid entity_id and new mass
    response = client.delete(f"/delete_user/{user_id}")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message and new mass are correct
    assert response.json() == {"message": "User deleted successfully"}

# Test invalid user_id (user not found)
def test_update_user_not_found():
    # Send a PUT request with an invalid entity_id
    response = client.delete("/delete_user/999")

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "User not found"}
