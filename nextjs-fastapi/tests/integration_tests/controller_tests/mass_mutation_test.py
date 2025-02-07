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


@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = 'sqlite:///nextjs-fastapi/db/capstone_db.db'
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
def test_material_consume_success(setup_database):
    session = setup_database

    repository = MaterialRepository(session)

    material = repository.get_material_by_id(1)

    mass = material.mass
    link = material.supplier_link
    id = material.material_type_id
    shelf = material.shelf_id

    # Send a PUT request with valid entity_id and new mass
    response = client.patch("/consume_mass/1", json={"mass_change": 5.0})

    print(f"Response: {response.json()}")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message and new mass are correct
    assert response.json() == {"message": f"{5.0} grams consumed"}

    repository.update_material(material, mass=mass, supplier_link=link, material_type_id=id, shelf_id=1)


# Test invalid material_id (material not found)
def test_material_consume_not_found():

    # Send a PUT request with valid entity_id and new mass
    response = client.patch("/consume_mass/-1", json={"mass_change": 5.0})

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "Material not found"}


# Test valid mass update
def test_material_replenish_success(setup_database):
    session = setup_database

    repository = MaterialRepository(session)

    material = repository.get_material_by_id(1)
    mass = material.mass
    link = material.supplier_link
    id = material.material_type_id
    shelf = material.shelf_id


    # Send a PUT request with valid entity_id and new mass
    response = client.patch("/replenish_mass/1", json={"mass_change": 5.0})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message and new mass are correct
    assert response.json() == {"message": f"{5.0} grams replenished"}

    repository.update_material(material, mass=mass, supplier_link=link, material_type_id=id, shelf_id=1)


# Test invalid material_id (material not found)
def test_material_replenish_not_found():

    # Send a PUT request with valid entity_id and new mass
    response = client.patch("/replenish_mass/-1", json={"mass_change": 5.0})

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "Material not found"}