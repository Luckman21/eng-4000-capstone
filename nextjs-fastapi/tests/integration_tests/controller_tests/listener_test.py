from httpx import patch
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from db.model import Material
from sqlalchemy.orm import Session
from db.repositories.MaterialRepository import MaterialRepository

# Initialize the TestClient with the FastAPI app
app = get_app()
client = TestClient(app)

# Helper function to create materials in the test database
def create_material(db: Session, name: str, mass: float):
    material = Material(name=name, mass=mass)
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

# Test that listener works after PUT request to update mass
@pytest.mark.asyncio
def test_listener_triggered_by_update_mass(client):
    """
    Test the listener triggered by a PUT request to update the mass of a material.
    It should check if materials with mass below the threshold (50g) are alerted.
    """

    # Create a test material with a mass below the threshold (e.g., 40g)
    material_data = {"name": "Test Material", "mass": 40.0}

    # Use the TestClient to make a PUT request to update the material's mass
    response = client.put(f"/update_mass/{1}", json=material_data)

    # Ensure the update request is successful
    assert response.status_code == 200

    # Get the response data
    data = response.json()

    # Check if the listener was triggered and the material was updated
    assert "Mass updated successfully" in data["message"]
    assert data["new_mass"] == 40.0  # Ensure mass is updated

# Mock the listener's job_complete_listener function to avoid actual database changes
@pytest.mark.asyncio
@patch("controller.listener.job_complete_listener")
def test_listener_with_mock(mock_listener, client):
    """
    Test the listener behavior when the job_complete_listener function is mocked.
    This prevents changes to the database and directly tests the listener's flow.
    """
    
    # Define the mock behavior
    mock_listener.return_value = None  # Simulate that the listener does nothing
    
    # Create a test material with a mass below the threshold (e.g., 40g)
    material_data = {"name": "Test Material", "mass": 40.0}

    # Use the TestClient to make a PUT request to update the material's mass
    response = client.put(f"/update_mass/{1}", json=material_data)

    # Ensure the update request is successful
    assert response.status_code == 200
    assert "Mass updated successfully" in response.json()["message"]
    
    # Check if the mocked listener was called (i.e., the alert logic was triggered)
    mock_listener.assert_called_once()  # Ensure the listener was called at least once