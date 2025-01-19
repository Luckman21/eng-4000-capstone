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
from backend.controller.constants import DATABASE_URL_TEST 

@pytest.fixture(scope="module") 
def setup_database(request): 
    DATABASE_URL = DATABASE_URL_TEST 
    engine = create_engine(DATABASE_URL, echo=True) 
    
    Base.metadata.create_all(engine) 
    
    Session = sessionmaker(bind=engine) 
    
    session = Session()
    
    def cleanup(): 
        session.close()  
    
    yield session 
    
client = TestClient(get_app()) 
    
def test_get_all_materials(setup_database): 
    session = setup_database 
    material_type = session.query(MaterialType).filter_by(type_name="Plastic").first() 
    
    if not material_type: 
        material_type = MaterialType(type_name="Plastic") 
        session.add(material_type) 
        session.commit() 
    
    material = session.query(Material).filter_by(supplier_link="Dummy Material").first()
    
    if not material: 
        material = Material( supplier_link="Dummy Material", colour="Red", mass=10.5, material_type_id=material_type.id, shelf_id=1 )
        session.add(material) 
        session.commit() 
        
    response = client.get("/materials") 
    assert response.status_code == 200 
    
    materials = response.json() 
    
    assert any( m["supplier_link"] == "Dummy Material" and m["colour"] == "Red" and m["mass"] == 10.5 for m in materials )
    session.query(MaterialType).filter_by(type_name="Plastic").delete()
    session.query(Material).filter_by(supplier_link="Dummy Material").delete()
    session.commit()
    session.close()