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
    DATABASE_URL = constants.DATABASE_URL_TEST
    engine = create_engine(constants.DATABASE_URL_TEST, echo=True)

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
def test_create_material_type_success(setup_database):
    session = setup_database

    db_count = session.query(MaterialType).count()

    repository = MaterialTypeRepository(session)

    # Send a PUT request with valid entity_id and new mass
    response = client.post("material_types/create_mattype", json={"type_name": "Elastic Plastic"})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message and new mass are correct
    assert response.json() == {"message": "Material Type successfully created"}

    type = session.query(MaterialType).filter_by(type_name="Elastic Plastic").delete()
    session.commit()

    assert db_count == session.query(MaterialType).count()

# Test invalid user_id (user not found)
def test_create_material_type_not_found(setup_database):

    session = setup_database

    db_count = session.query(MaterialType).count()
    repository = MaterialTypeRepository(session)
    repository.create_material_type(
        type_name="Dummy Material Type 2"
    )

    # Send a PUT request with an invalid entity_id
    response = client.post("material_types/create_mattype", json={"type_name" : "Dummy Material Type 2"})

    # Assert that the response status code is 404
    assert response.status_code == 404

    # Assert that the response contains the correct error message
    assert response.json() == {"detail": "Material Type already exists"}
    session.query(MaterialType).filter_by(type_name="Dummy Material Type 2").delete()
    session.commit()
    assert db_count == session.query(MaterialType).count()
