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
from db.repositories.UserRepository import UserRepository
from backend.controller import constants

@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL_TEST
    engine = create_engine(constants.DATABASE_URL_TEST, echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()

# Initialize the TestClient to simulate schemas
client = TestClient(get_app())

# Test valid mass update
def test_create_user_success(setup_database):
    session = setup_database

    db_count = session.query(User).count()

    repository = UserRepository(session)

    # Send a PUT request with valid entity_id and new mass
    response = client.post("/create_user", json={"password": "123", "username": "Mickey Mouse", "email": "red3@email.com", "user_type_id": 1})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message and new mass are correct
    assert response.json() == {"message": "User successfully created"}

    user = session.query(User).filter_by(username="Mickey Mouse", email='red3@email.com').delete()
    session.commit()
    assert db_count == session.query(User).count()

# Test invalid user_id (user not found)
def test_create_user_not_found(setup_database):

    session = setup_database

    db_count = session.query(User).count()
    repository = UserRepository(session)
    repository.create_user(
        username="Dummy Material",
        email="red@email.com",
        password="123",
        user_type_id=1
    )

    # Send a PUT request with an invalid entity_id
    response = client.post("/create_user", json={"password": "123", "username": "Dummy Material", "email": "red@email.com","user_type_id": 1})

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "User already exists"}
    session.query(User).filter_by(username="Dummy Material").delete()
    session.commit()
    assert db_count == session.query(User).count()
