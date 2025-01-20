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
from db.model.Shelf import Shelf

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

    db_count = session.query(Material).count()

    # Create sample MaterialType data for foreign key reference
    material_type = MaterialType(type_name='Plastic')  # Initialize MaterialType correctly
    session.add(material_type)
    session.commit()

    dummy_material = Material(
        supplier_link="Dummy Material",
        colour="Red",
        mass=10.5,
        material_type_id=material_type.id,
        shelf_id = 1
    )
    session.add(dummy_material)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(Material).filter_by(supplier_link="Dummy Material").delete()
        session.query(MaterialType).filter_by(type_name="Plastic").delete()
        session.commit()
        assert db_count == session.query(Material).count()

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
        supplier_link='Material 1',
        mass=10.5,
        material_type_id=material_type.id,
        shelf_id=1
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
    assert material.supplier_link == 'Material 1'
    assert material.mass == 10.5
    assert material.material_type_id == material_type.id
    assert material.shelf_id == 1

    session.query(Material).filter_by(supplier_link="Material 1").delete()
    session.commit()

# Test invalid mass (negative value) raises IntegrityError
def test_material_invalid_mass(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType

    material = Material(
        colour='Blue',
        supplier_link='Material 2',
        mass=-5.0,  # Invalid mass (negative value)
        material_type_id=material_type.id,
        shelf_id = 1
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
        supplier_link='Material 3',
        mass=8.5,
        material_type_id=material_type.id,
        shelf_id = 1
    )

    material.setColour('Green')
    assert material.colour == 'Green'

    # Invalid input: colour must be a string
    with pytest.raises(ValueError):
        material.setColour(123)  # Passing an integer instead of a string
        session.query(Material).filter_by(supplier_link="Material 3").delete()
        session.commit()

# Test setName method with valid and invalid inputs
def test_set_supplier_link(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType
    material = Material(
        colour='Yellow',
        supplier_link='Material 4',
        mass=5.0,
        material_type_id=material_type.id,
        shelf_id = 1
    )

    material.setSupplierLink('New Material')
    assert material.supplier_link == 'New Material'

    # Invalid input: name must be a string
    with pytest.raises(ValueError):
        material.setSupplierLink(123)  # Passing an integer instead of a string
        session.query(Material).filter_by(supplier_link="New Material").delete()
        session.commit()

    # The dummy data will be rolled back after the test



def test_update_material_shelf(session):

    # Add a new shelf for the test
    new_shelf = Shelf(humidity_pct=60.0, temperature_cel=25.0)
    session.add(new_shelf)
    session.commit()

    # Fetch the dummy material and update its shelf
    material_to_update = session.query(Material).filter_by(supplier_link="Dummy Material").first()
    assert material_to_update is not None

    material_to_update.shelf_id = new_shelf.id
    session.commit()

    # Verify that the material's shelf was updated
    updated_material = session.query(Material).filter_by(supplier_link="Dummy Material").first()
    assert updated_material.shelf_id == new_shelf.id

    queried_shelf = session.query(Shelf).filter_by(id=new_shelf.id).first()
    assert queried_shelf is not None
    assert queried_shelf.humidity_pct == 60.0


# Example test case 4: Test a material update
def test_update_material_colour(session):
    # Get the session from the fixture

    # Fetch an existing material and update its data
    material_to_update = session.query(Material).filter_by(supplier_link="Dummy Material").first()
    assert material_to_update is not None

    material_to_update.setColour("Tangarine")
    assert material_to_update.colour == "Tangarine"

# Test setMaterialTypeID method with valid and invalid inputs
def test_set_material_type_id(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType
    another_material_type = MaterialType(type_name='Metal')  # Use 'type_name' for consistency
    session.add(another_material_type)
    session.commit()  # Commit to generate a new ID for the new material type

    material = Material(
        colour='Grey',
        supplier_link='Material 5',
        mass=3.0,
        material_type_id=material_type.id,
        shelf_id = 1
    )

    # Update material's type
    material.setMaterialTypeID(another_material_type.id)
    assert material.material_type_id == another_material_type.id

    # Invalid input: should raise ValueError if not passed a MaterialType instance
    with pytest.raises(ValueError):
        material.setMaterialTypeID('NonMaterialType')  # Passing an invalid type (string)
        session.query(Material).filter_by(supplier_link="Material 5").delete()
        session.query(MaterialType).filter_by(type_name="Metal").delete()
        session.commit()


# Test getAll method for retrieving all materials
def test_get_all_materials(session):
    material_type = session.query(MaterialType).first()  # Get the first MaterialType

    material1 = Material(
        colour='White',
        supplier_link='Material 6',
        mass=12.0,
        material_type_id=material_type.id,
        shelf_id = 1
    )

    material2 = Material(
        colour='Black',
        supplier_link='Material 7',
        mass=15.0,
        material_type_id=material_type.id,
        shelf_id = 1
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
    print(materials[0].supplier_link)
    assert len(materials) == 3  # We added three materials (first in test 1, with Material 1)
    assert materials[0].supplier_link == 'Dummy Material'
    assert materials[1].supplier_link == 'Material 6'
    assert materials[2].supplier_link == 'Material 7'

    # Clean up
    session.query(Material).filter_by(supplier_link="Material 7").delete()
    session.query(Material).filter_by(supplier_link="Dummy Material").delete()
    session.query(Material).filter_by(supplier_link="Material 6").delete()
    session.commit()