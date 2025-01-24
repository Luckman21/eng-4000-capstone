import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from db.model.base import Base
from db.model.Material import Material
from db.model.MaterialType import MaterialType
from db.repositories.MaterialRepository import MaterialRepository
from backend.controller.listener import job_complete_listener
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import scoped_session

# Define the test database URL (using the provided one)
DATABASE_URL = 'sqlite:///nextjs-fastapi/db/capstone_db.db'

# Create the engine and session for SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(TestingSessionLocal)

# Step 1: Setup Database for Testing (no need for table creation)
@pytest.fixture(scope="module")
def setup_database():
    session = TestingSessionLocal()

    # Add a dummy material type (if not already in the database)
    dummy_material_type = MaterialType(type_name="TestPlastic")
    session.add(dummy_material_type)
    session.commit()

    # Add some test materials (one below threshold and one above)
    dummy_material1 = Material(
        name="Test Material 1",
        colour="Blue",
        mass=5.0,  # Below the threshold
        material_type_id=dummy_material_type.id
    )

    dummy_material2 = Material(
        name="Test Material 2",
        colour="Green",
        mass=60.0,  # Above the threshold
        material_type_id=dummy_material_type.id
    )

    session.add(dummy_material1)
    session.add(dummy_material2)
    session.commit()

    yield session # yield session so tests can run

    # Step 2: Clean up by removing the test materials and test material type
    session.query(Material).filter(Material.name.in_(["Test Material 1", "Test Material 2"])).delete()
    session.query(MaterialType).filter(MaterialType.type_name == "TestPlastic").delete()
    session.commit()
    session.close()

# Step 3: Test the Listener for Low Mass Materials
@pytest.mark.asyncio
async def test_job_complete_listener_low_mass(setup_database):
    """
    Test the listener functionality when a material is updated with a mass below the threshold.
    """
    session = setup_database

    # Fetch the material with mass below the threshold (5.0g)
    material = session.query(Material).filter_by(name="Test Material 1").first()

    # Mock the mapper and connection arguments that job_complete_listener expects
    mapper = MagicMock()  # Mock object for mapper
    connection = MagicMock()  # Mock object for connection

    # Call the job_complete_listener (which will be triggered by an update)
    alert_materials = await job_complete_listener(mapper, connection, material)

    # Assert that the listener triggered for the low mass material
    assert len(alert_materials) == 2  # Only 1 material should be below threshold
    assert alert_materials[1].name == "Test Material 1"
    assert alert_materials[1].mass == 5.0

# Step 4: Test the Listener for High Mass Materials (no alert)
@pytest.mark.asyncio
async def test_job_complete_listener_high_mass(setup_database):
    """
    Test the listener functionality when a material is updated with a mass above the threshold.
    """
    session = setup_database

    # Fetch the material with mass above the threshold (60.0g)
    material = session.query(Material).filter_by(name="Test Material 2").first()

    # Mock the mapper and connection arguments that job_complete_listener expects
    mapper = MagicMock()  # Mock object for mapper
    connection = MagicMock()  # Mock object for connection

    # Call the job_complete_listener (which will be triggered by an update)
    alert_materials = await job_complete_listener(mapper, connection, material)

    # Assert that no materials are alerted for the high mass material
    assert len(alert_materials) == 2  # No material should be below the threshold