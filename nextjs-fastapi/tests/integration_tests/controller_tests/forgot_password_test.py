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
from db.model.base import Base
from backend.service.mailer.TempPasswordMailer import TempPasswordMailer
from backend.controller import constants


@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL
    engine = create_engine(DATABASE_URL, echo=True)

    Base.metadata.create_all(engine)

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

    def cleanup():
        session.query(User).filter_by(username="Dummy User").delete()
        session.commit()
        assert db_count == session.query(User).count()


    request.addfinalizer(cleanup)

    yield session
    session.close()


# Initialize the TestClient to simulate schemas
client = TestClient(get_app())


def test_email_temp_success(setup_database):
    session = setup_database

    user = session.query(User).filter_by(username="Dummy User").first()

    assert user is not None, "Dummy user should exist in the database"

    with mock.patch.object(TempPasswordMailer, 'send_notification') as mock_send:
        mock_send.return_value = None

        # Trigger the password reset
        response = client.post(f"access_management/forgot_password/", json={"email": user.email})

        assert response.status_code == 200
        mock_send.assert_called_once_with(user.email, mock.ANY)


# Test invalid user
def test_update_user_not_found():
    # Send a PUT request with an invalid entity_id
    response = client.post("access_management/forgot_password/", json={"email" : "fakest_email_of_all"})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
