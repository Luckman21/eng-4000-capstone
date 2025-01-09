import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from db.model.MaterialType import MaterialType
from db.model.base import Base

# Fixture to setup an in-memory database for testing
@pytest.fixture(scope='module')
def session():
    # Setup the in-memory SQLite database engine
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # Create all tables defined in Base

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Cleanup after test
    session.close()
    engine.dispose()

# Test case for MaterialType creation and initialization
def test_material_type_creation(session):
    # Create a valid MaterialType
    material_type = MaterialType(type_name='Plastic')
    session.add(material_type)
    
    session.commit()

    # Test that the material type was successfully added
    assert material_type.id is not None
    assert material_type.type_name == 'Plastic'

# Test case to check unique constraint on type_name
def test_material_type_unique_constraint(session):
    material_type1 = MaterialType(type_name='Plastic')
    material_type2 = MaterialType(type_name='Plastic')  # Duplicate name

    session.add(material_type1)
    
    # Explicit rollback before commit
    session.rollback()
    
    session.commit()

    # Try to add a second material type with the same name and check for IntegrityError
    session.add(material_type2)

    # Check for IntegrityError
    with pytest.raises(IntegrityError):
        session.commit()

# Test setName method with valid and invalid inputs
def test_set_name(session):
    material_type = MaterialType(type_name='Plastic')
    session.add(material_type)
    
    # Explicit rollback before commit
    session.rollback()
    
    session.commit()

    # Test valid input
    material_type.setName('Metal')
    assert material_type.type_name == 'Metal'

    # Test invalid input: should raise ValueError if name is not a string
    with pytest.raises(ValueError):
        material_type.setName(123)  # Passing an integer instead of a string

# Test getAll method for retrieving all material types
def test_get_all_material_types(session):
    material_type1 = MaterialType(type_name='Plastic')
    material_type2 = MaterialType(type_name='Metal')

    session.add(material_type1)

    # Explicit rollback before commit
    session.rollback()
    
    session.add(material_type2)
    
    session.commit()

    # Test the getAll method to fetch all material types
    material_types = MaterialType.getAll(MaterialType, session)
    assert len(material_types) == 2  # We added two material types
    assert material_types[0].type_name == 'Plastic'
    assert material_types[1].type_name == 'Metal'