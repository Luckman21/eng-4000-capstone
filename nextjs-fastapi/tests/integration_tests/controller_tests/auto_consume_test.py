import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from db.repositories.MaterialRepository import MaterialRepository
from unittest.mock import patch


# Fixture to set up the database
@pytest.fixture(scope='module')
def setup_database(request):
    from backend.controller import constants
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from db.model.base import Base

    DATABASE_URL = constants.DATABASE_URL
    engine = create_engine(DATABASE_URL, echo=True)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session
    session.close()


client = TestClient(get_app())

# Test valid QR display success
def test_qr_display_success(setup_database):
    session = setup_database
    repository = MaterialRepository(session)
    material = repository.get_material_by_id(1)

    mass = material.mass
    name = material.material_type.type_name
    colour = material.colour
    id = material.id

    # Mock the get_scale_listener to return a predefined value
    with patch("backend.controller.routers.qr.get_scale_listener") as mock_get_listener:

        mock_instance = mock_get_listener.return_value

        # Simulate receiving an MQTT message
        payload = "2|"+str(mass)
        mock_instance.process_message(payload)
        mock_instance.get_latest_value.return_value = mass

        response = client.get(f"/qr_display/{id}")
        assert response.status_code == 200

        response_as_json = response.json()
        assert response_as_json['material_type_name'] == name
        assert response_as_json['material']['colour'] == colour
        assert response_as_json['material']['mass'] == mass
        assert response_as_json['material']['id'] == id


def test_material_consume_not_found():
    response = client.get("/qr_display/-1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Material not found"}


@pytest.mark.parametrize("mock_mass", [0.0, -5.0])
def test_auto_consume_mass_throws_500(mock_mass):
    with patch("backend.controller.routers.qr.get_mass_from_scale", return_value=mock_mass):
        response = client.get("/qr_display/1")
        assert response.status_code == 500
        assert response.json() == {"detail": "Mass reading on scale is less than or equal to zero"}