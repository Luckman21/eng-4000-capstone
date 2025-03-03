# tests/test_update_mass.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.Material import Material
from db.model.MaterialType import MaterialType
from db.model.base import Base
from db.repositories.MaterialRepository import MaterialRepository
from backend.controller import constants
from unittest.mock import patch


@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL_TEST
    engine = create_engine(DATABASE_URL, echo=True)

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
def test_qr_display_success(setup_database):
    session = setup_database

    repository = MaterialRepository(session)

    material = repository.get_material_by_id(1)

    mass = material.mass
    name = material.material_type.type_name
    colour = material.colour

    # Send a PUT request with valid entity_id and new mass
    response = client.get("/qr_display/1")

    # Assert that the response status code is 200
    assert response.status_code == 200

    response_as_json = response.json()

    # Assert that the response message and new mass are correct
    assert response_as_json['material_type_name'] == name
    assert response_as_json['colour'] == colour


# Test invalid material_id (material not found)
def test_material_consume_not_found():

    # Send a PUT request with valid entity_id and new mass
    response = client.get("/qr_display/-1")

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "Material not found"}


@pytest.mark.parametrize("mock_mass", [0.0, -5.0])
def test_auto_consume_mass_throws_500(mock_mass):
    """Test that the endpoint returns 500 when mass_on_the_scale is ≤ 0.0"""
    with patch("backend.controller.main.get_mass_from_scale", return_value=mock_mass):
        response = client.get("/qr_display/1")
        assert response.status_code == 500
        assert response.json() == {"detail": "Mass reading on scale is less than or equal to zero"}

