# tests/test_update_mass.py

import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app  # Import your FastAPI app

# Initialize the TestClient to simulate schemas
client = TestClient(get_app)

# Test valid mass update
def test_update_mass_success():
    # Send a PUT request with valid entity_id and new mass
    response = client.put("/update_mass/1", json={"mass": 200.0})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message and new mass are correct
    assert response.json() == {"message": "Mass updated successfully", "new_mass": 200.0}

# Test invalid material_id (material not found)
def test_update_mass_not_found():
    # Send a PUT request with an invalid entity_id
    response = client.put("/update_mass/999", json={"mass": 200.0})

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "Mass entity not found"}
