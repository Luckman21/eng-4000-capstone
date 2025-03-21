# tests/test_update_mass.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from fastapi import status
from db.model.User import User
from db.model.base import Base
from db.repositories.UserRepository import UserRepository

@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL
    engine = create_engine(DATABASE_URL, echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()


@pytest.mark.asyncio
async def test_login_success():

    #TODO make dedicated dummy user

    client = TestClient(get_app())
    response = client.post(
        "access_management/login",
        data={"username": f"water_123", "password": f"Gucci2001"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Login successful"}
    assert "access_token" in response.cookies, "Access token cookie is missing"


@pytest.mark.asyncio
async def test_login_failure():
    client = TestClient(get_app())
    response = client.post(
        "access_management/login",
        data={"username": "invalid_user", "password": "wrong_password"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid username or password"
    assert "access_token" not in response.cookies, "Access token should not be set for invalid login"


@pytest.mark.asyncio
async def test_logout():
    client = TestClient(get_app())
    # First, simulate a login to set the cookie
    login_response = client.post(
        "access_management/login",
        data={"username": "water_123", "password": "Gucci2001"},
    )
    assert login_response.status_code == status.HTTP_200_OK
    assert "access_token" in login_response.headers.get("set-cookie", "")

    # Now, log out
    logout_response = client.post("access_management/logout")

    assert logout_response.status_code == status.HTTP_200_OK
    assert logout_response.json() == {"message": "Logged out successfully"}

    # Check if the cookie is being cleared
    set_cookie_header = logout_response.headers.get("set-cookie", "")
    assert "access_token=" in set_cookie_header  # Cookie exists
    assert "Max-Age=0" in set_cookie_header or "expires=" in set_cookie_header  # Expired immediately


@pytest.mark.asyncio
async def test_logout_without_cookie():
    client = TestClient(get_app())
    # Log out without logging in first
    logout_response = client.post("access_management/logout")

    assert logout_response.status_code == status.HTTP_200_OK
    assert logout_response.json() == {"message": "Logged out successfully"}

    # There should be no valid cookie
    set_cookie_header = logout_response.headers.get("set-cookie", "")
    assert "access_token=" in set_cookie_header  # Cookie should still exist but be expired
    assert "Max-Age=0" in set_cookie_header or "expires=" in set_cookie_header  # Expired immediately
