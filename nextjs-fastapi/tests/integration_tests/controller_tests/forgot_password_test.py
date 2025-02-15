# tests/test_update_mass.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from unittest import mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.User import User
from db.model.UserType import UserType
from db.model.base import Base
from db.repositories.MaterialRepository import MaterialRepository
from backend.service.mailer.TempPasswordMailer import TempPasswordMailer
from backend.controller import constants

@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL_TEST
    engine = create_engine(DATABASE_URL, echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    db_count = session.query(User).count()

    dummy_user = User(
        username="Dummy User",
        email="lucafili@my.yorku.ca",
        password="123",
        user_type_id=1
    )
    session.add(dummy_user)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(User).filter_by(username="Dummy User").delete()
        session.commit()
        assert db_count == session.query(User).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()


# Initialize the TestClient to simulate schemas
client = TestClient(get_app())

def test_email_temp_success(setup_database):
    session = setup_database

    user = session.query(User).filter_by(username="Dummy User").first()

    assert user is not None, "Dummy user should exist in the database"

    with mock.patch.object(TempPasswordMailer, 'send_notification') as mock_send:
        mock_send.return_value = None  # The mocked method doesn't need to return anything

        # Trigger the password reset
        response = client.post(f"/forgot_password/", json={"email": user.email})

        # Assert the status code is 200
        assert response.status_code == 200

        # Ensure send_notification was called once
        mock_send.assert_called_once_with(user.email, mock.ANY)  # Check if the method was called with correct args


# Test invalid user
def test_update_user_not_found():
    # Send a PUT request with an invalid entity_id
    response = client.post("/forgot_password/", json={"email" : "fakest_email_of_all"})

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "User not found"}
