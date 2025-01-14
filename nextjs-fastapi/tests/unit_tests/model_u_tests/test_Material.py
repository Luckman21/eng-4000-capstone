import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from db.model.Material import Material
from db.model.MaterialType import MaterialType
from db.model.base import Base

# Use an existing database instead of an in-memory one
@pytest.fixture(scope='module')
def session():
    # Setup the in-memory SQLite database engine
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # Create all tables defined in Base

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create sample MaterialType data for foreign key reference
    material_type = MaterialType(type_name='Plastic')  # Initialize MaterialType correctly
    session.add(material_type)
    session.commit()

    dummy_material = Material(
        name="Dummy Material",
        colour="Red",
        mass=10.5,
        material_type_id=dummy_material_type.id
    )
    session.add(dummy_material)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(Material).filter_by(name="Dummy Material").delete()
        session.query(MaterialType).filter_by(type_name="Plastic").delete()
        session.commit()

    yield session

    # Cleanup after test
    session.close()
    engine.dispose()

# Test case for Material creation and initialization
def test_material_creation(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType

    # Create a valid Material
    material = Material(
        colour='Red',
        name='Material 1',
        mass=10.5,
        material_type_id=material_type.id
    )

    session.add(material)
    try:
        session.commit()  # Commit changes
    except IntegrityError as e:
        session.rollback()  # Rollback the session if there's an exception
        pytest.fail(f"IntegrityError: {e}")

    # Test that the material was successfully added
    assert material.id is not None
    assert material.colour == 'Red'
    assert material.name == 'Material 1'
    assert material.mass == 10.5
    assert material.material_type_id == material_type.id

# Test invalid mass (negative value) raises IntegrityError
def test_material_invalid_mass(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType

    material = Material(
        colour='Blue',
        name='Material 2',
        mass=-5.0,  # Invalid mass (negative value)
        material_type_id=material_type.id
    )

    session.add(material)

    # Check for IntegrityError due to negative mass constraint (CheckConstraint)
    with pytest.raises(IntegrityError):
        session.commit()  # This should raise IntegrityError due to the mass constraint
    session.rollback()

# Test setColour method with valid and invalid inputs
def test_set_colours(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType
    material = Material(
        colour='Red',
        name='Material 3',
        mass=8.5,
        material_type_id=material_type.id
    )

    material.setColour('Green')
    assert material.colour == 'Green'

    # Invalid input: colour must be a string
    with pytest.raises(ValueError):
        material.setColour(123)  # Passing an integer instead of a string

# Test setName method with valid and invalid inputs
def test_set_name(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType
    material = Material(
        colour='Yellow',
        name='Material 4',
        mass=5.0,
        material_type_id=material_type.id
    )

    material.setName('New Material')
    assert material.name == 'New Material'

    # Invalid input: name must be a string
    with pytest.raises(ValueError):
        material.setName(123)  # Passing an integer instead of a string
    inserted_shelf = session.query(Shelf).filter_by(id=inserted_material.shelf_id).first()
    assert inserted_shelf is not None
    assert inserted_shelf.humidity_pct == 50.0

    # The dummy data will be rolled back after the test


def test_update_material_shelf(setup_database):
    session = setup_database

    # Add a new shelf for the test
    new_shelf = Shelf(humidity_pct=60.0, temperature_cel=25.0)
    session.add(new_shelf)
    session.commit()

    # Fetch the dummy material and update its shelf
    material_to_update = session.query(Material).filter_by(name="Dummy Material").first()
    assert material_to_update is not None

    material_to_update.shelf_id = new_shelf.id
    session.commit()

    # Verify that the material's shelf was updated
    updated_material = session.query(Material).filter_by(name="Dummy Material").first()
    assert updated_material.shelf_id == new_shelf.id

    queried_shelf = session.query(Shelf).filter_by(id=new_shelf.id).first()
    assert queried_shelf is not None
    assert queried_shelf.humidity_pct == 60.0


# Example test case 4: Test a material update
def test_update_material_colour(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    material_to_update = session.query(Material).filter_by(name="Dummy Material").first()
    assert material_to_update is not None

# Test setMaterialTypeID method with valid and invalid inputs
def test_set_material_type_id(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType
    another_material_type = MaterialType(type_name='Metal')  # Use 'type_name' for consistency
    session.add(another_material_type)
    session.commit()  # Commit to generate a new ID for the new material type

    material = Material(
        colour='Grey',
        name='Material 5',
        mass=3.0,
        material_type_id=material_type.id
    )

    # Update material's type
    material.setMaterialTypeID(another_material_type)
    assert material.material_type_id == another_material_type.id
    assert material.material_type == another_material_type

    # Invalid input: should raise ValueError if not passed a MaterialType instance
    with pytest.raises(ValueError):
        material.setMaterialTypeID('NonMaterialType')  # Passing an invalid type (string)

# Test getAll method for retrieving all materials
def test_get_all_materials(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType

    material1 = Material(
        colour='White',
        name='Material 6',
        mass=12.0,
        material_type_id=material_type.id
    )

    material2 = Material(
        colour='Black',
        name='Material 7',
        mass=15.0,
        material_type_id=material_type.id
    )

    session.add(material1)
    session.add(material2)
    try:
        session.commit()  # Commit changes
    except IntegrityError as e:
        session.rollback()  # Rollback the session if there's an exception
        pytest.fail(f"IntegrityError: {e}")

    # Test the getAll method to fetch all materials
    materials = Material.getAll(Material, session)
    assert len(materials) == 3  # We added three materials (first in test 1, with Material 1)
    assert materials[0].name == 'Material 1'
    assert materials[1].name == 'Material 6'
    assert materials[2].name == 'Material 7'