import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db.dependencies import get_db
from db.model.base import Base
from db.model.Material import Material
from db.model.MaterialType import MaterialType

DATABASE_URL = 'sqlite:///nextjs-fastapi/db/capstone_db.db'
engine = create_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database(request):
    
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    
    dummy_material_type = MaterialType(type_name="TestPlastic")
    session.add(dummy_material_type)
    session.commit()

    dummy_material1 = Material(
        name="Test Material 1",
        colour="Blue",
        mass=5.0,
        material_type_id=dummy_material_type.id
    )

    dummy_material2 = Material(
        name="Test Material 2",
        colour="Green",
        mass=7.5,
        material_type_id=dummy_material_type.id
    )

    session.add(dummy_material1)
    session.add(dummy_material2)
    session.commit()

    yield session

    session.query(Material).delete()
    session.query(MaterialType).delete()
    session.commit()
    session.close()

    Base.metadata.drop_all(bind=engine)


def get_Allmaterials_test(setup_database):
    response = client.get("/materials")

    assert response.status_code == 200

    materials = response.json()
    assert len(materials) == 2

    assert materials[0]["name"] == "Test Material 1"
    assert materials[0]["colour"] == "Blue"
    assert materials[0]["mass"] == 5.0

    assert materials[1]["name"] == "Test Material 2"
    assert materials[1]["colour"] == "Green"
    assert materials[1]["mass"] == 7.5