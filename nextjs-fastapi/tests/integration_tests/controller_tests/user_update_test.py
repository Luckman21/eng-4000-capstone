import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from unittest import mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.base import Base
from db.repositories.UserRepository import UserRepository
from backend.service.mailer.PasswordChangeMailer import PasswordChangeMailer
from backend.controller import constants


@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL
    engine = create_engine(DATABASE_URL, echo=True)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session
    session.close()


# Initialize the TestClient to simulate schemas
client = TestClient(get_app())


# Test valid mass update
def test_update_user_success(setup_database):
    session = setup_database

    repository = UserRepository(session)

    user = repository.get_user_by_id(1)
    email = user.email
    username = user.username
    id = user.user_type_id

    with mock.patch.object(PasswordChangeMailer, 'send_notification') as mock_send:
        mock_send.return_value = None  # The mocked method doesn't need to return anything

        # Send a PUT request with valid entity_id and new mass
        response = client.put("users/update_user/1", json={"username": "hi", "email": None, "password": "None", "user_type_id": 1})

        # Assert that the response status code is 200
        assert response.status_code == 200

        # Assert that the response message and new mass are correct
        assert response.json()["message"] == "User updated successfully"

        mock_send.assert_called_once_with(user.email)  # Check if the method was called with correct args

    response = client.put("users/update_user/1",
                          json={"username": username, "email": None, "password": "jones7788", "user_type_id": 1})
    user = repository.get_user_by_id(1)
    assert user.username == username


# Test invalid material_id (material not found)
def test_update_user_not_found():
    # Send a PUT request with an invalid entity_id
    response = client.put("users/update_user/9999", json={"username": "hi", "email": "cookies@gmail.com", "password": None, "user_type_id": 2})

    assert response.status_code == 404


    assert response.json() == {"detail": "User not found"}
