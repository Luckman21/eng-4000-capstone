import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.base import Base
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from backend.controller import constants


@pytest.fixture(scope='module')
def setup_database(request):
    DATABASE_URL = constants.DATABASE_URL
    engine = create_engine(DATABASE_URL, echo=True)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session
    session.close()


client = TestClient(get_app())

# Test valid mass update
def test_update_material_type_success(setup_database):
    session = setup_database

    repository = MaterialTypeRepository(session)

    material_type = repository.get_material_type_by_id(1)
    type_name = material_type.type_name

    # Send a PUT request with valid entity_id and new mass
    response = client.put("material_types/update_mattype/1", json={"type_name" : "Cookies"})

    assert response.status_code == 200
    assert response.json() == {"message": "Material Type updated successfully"}

    client.put("material_types/update_mattype/1", json={"type_name" : f'{material_type.type_name}'})

    material_type = repository.get_material_type_by_id(1)

    assert material_type.type_name == type_name

# Test invalid material_id (material not found)
def test_update_material_type_not_found():
    # Send a PUT request with an invalid entity_id
    response = client.put("material_types/update_mattype/999", json={"type_name" : "Turtles"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Material Type not found"}
