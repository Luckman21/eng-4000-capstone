import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.User import User
from db.model.base import Base
from db.repositories.UserRepository import UserRepository
from backend.controller import constants


@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL
    engine = create_engine(constants.DATABASE_URL, echo=True)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session
    session.close()

# Initialize the TestClient to simulate schemas
client = TestClient(get_app())


def test_create_user_success(setup_database):
    session = setup_database

    db_count = session.query(User).count()

    repository = UserRepository(session)

    # Send a PUT request with valid entity_id and new mass
    response = client.post("users/create_user", json={"password": "123", "username": "Mickey Mouse", "email": "red3@email.com", "user_type_id": 1})

    assert response.status_code == 200
    assert response.json() == {"message": "User successfully created"}

    user = session.query(User).filter_by(username="Mickey Mouse", email='red3@email.com').delete()
    session.commit()
    assert db_count == session.query(User).count()


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
    response = client.post("users/create_user", json={"password": "123", "username": "Dummy Material", "email": "red@email.com","user_type_id": 1})

    assert response.status_code == 404

    assert response.json() == {"detail": "User already exists"}
    session.query(User).filter_by(username="Dummy Material").delete()
    session.commit()
    assert db_count == session.query(User).count()
