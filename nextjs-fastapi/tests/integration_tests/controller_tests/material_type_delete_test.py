# tests/test_update_mass.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.MaterialType import MaterialType
from db.model.base import Base
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from backend.controller import constants

@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL
    engine = create_engine(DATABASE_URL, echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    db_count = session.query(MaterialType).count()

    # Add some dummy data
    dummy_material_type = MaterialType(type_name="Plastic2")
    session.add(dummy_material_type)
    session.commit()


    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(MaterialType).filter_by(type_name="Plastic2").delete()
        session.commit()
        assert db_count == session.query(MaterialType).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()


# Initialize the TestClient to simulate schemas
client = TestClient(get_app())

# Test valid mass update
def test_delete_material_type_success(setup_database):
    session = setup_database

    material_type = session.query(MaterialType).filter_by(type_name="Plastic2").first()

    assert material_type is not None, "Dummy material type should exist in the database"

    material_type_id = material_type.id

    # Send a PUT request with valid entity_id and new mass
    response = client.delete(f"/delete_mattype/{material_type_id}")
    print(response)
    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message and new mass are correct
    assert response.json() == {"message": "Material Type deleted successfully"}

# Test invalid material_id (material not found)
def test_update_material_type_not_found():
    # Send a PUT request with an invalid entity_id
    response = client.delete("/delete_mattype/999")

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "Material Type not found"}
