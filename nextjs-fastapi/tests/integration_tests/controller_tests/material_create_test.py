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
def test_create_material_success(setup_database):
    session = setup_database

    db_count = session.query(Material).count()

    repository = MaterialRepository(session)

    # Send a PUT request with valid entity_id and new mass
    response = client.put("/create_material", json={"mass": 200.0, "name": "Mickey Mouse", "colour": "red", "material_type_id": 1})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message and new mass are correct
    assert response.json() == {"message": "Material successfully created"}

    material = session.query(Material).filter_by(name="Mickey Mouse", mass= 200.0, colour='red').delete()
    session.commit()
    assert db_count == session.query(Material).count()

# Test invalid material_id (material not found)
def test_update_material_not_found(setup_database):

    session = setup_database

    db_count = session.query(Material).count()
    repository = MaterialRepository(session)
    repository.create_material(
        name="Dummy Material",
        colour="Red",
        mass=10.5,
        material_type_id=1
    )

    # Send a PUT request with an invalid entity_id
    response = client.put("/create_material", json={"mass": 10.5, "name": "Dummy Material", "colour": "Red", "material_type_id": 1})

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "Material already exists"}
    session.query(Material).filter_by(name="Dummy Material").delete()
    session.commit()
    assert db_count == session.query(Material).count()
