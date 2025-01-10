import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pytest
from fastapi.testclient import TestClient
from backend.controller.main import get_app
from backend.controller.dependencies import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.base import Base
from db.model.Material import Material
from db.model.MaterialType import MaterialType

@pytest.fixture(scope="module")
def setup_database(request):
    DATABASE_URL = 'sqlite:///nextjs-fastapi/db/capstone_db.db'
    engine = create_engine(DATABASE_URL, echo=True)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    def cleanup():
        session.close()
        Base.metadata.drop_all(engine)

    yield session

client = TestClient(get_app())


def get_Allmaterials_test(setup_database):
    session = setup_database

    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first()

    if not material_type:
        material_type = MaterialType(type_name="Plastic")
        session.add(material_type)
        session.commit()
    
    material = session.query(Material).filter_by(name="Dummy Material").first()

    if not material:
        material = Material(
            name="Dummy Material",
            colour="Red",
            mass=10.5,
            material_type_id=material_type.id
        )
        session.add(material)
        session.commit()

    response = client.get("/materials")

    assert response.status_code == 200

    materials = response.json()

    assert any(
        m["name"] == "Dummy Material" and 
        m["colour"] == "Red" and 
        m["mass"] == 10.5 for m in materials
        )


def get_Allmaterials_test_empty(setup_database):
    session = setup_database

    session.query(Material).delete()
    session.commit()

    response = client.get("/materials")

    assert response.status_code == 200

    assert response.json() == []
