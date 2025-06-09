import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.base import Base
from db.repositories.MaterialRepository import MaterialRepository
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
def test_update_material_success(setup_database):
    session = setup_database

    repository = MaterialRepository(session)

    material = repository.get_material_by_id(1)
    mass = material.mass
    link = material.supplier_link
    id = material.material_type_id
    shelf = material.shelf_id

    # Send a PUT request with valid entity_id and new mass
    response = client.put("materials/update_material/1", json={"mass": 200.0, "supplier_link": "Mickey Mouse", "colour": None, "material_type_id": 6, "shelf_id" : 1})

    assert response.status_code == 200
    assert response.json() == {"message": "Material updated successfully"}

    repository.update_material(material, mass=mass, supplier_link=link, material_type_id=id, shelf_id=1)


# Test invalid material_id (material not found)
def test_update_material_not_found():
    # Send a PUT request with an invalid entity_id
    response = client.put("materials/update_material/999", json={"mass": 200.0, "supplier_link": "Mickey Mouse", "colour": None, "material_type_id": None, "shelf_id" : 1})

    assert response.status_code == 404
    assert response.json() == {"detail": "Material not found"}
