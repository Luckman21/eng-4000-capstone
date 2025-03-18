import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model.Warning import Warning
from db.model.base import Base
from db.repositories.WarningRepository import WarningRepository
from backend.controller import constants

# Use an existing database instead of an in-memory one
@pytest.fixture(scope='module')
def setup_database(request):
    engine = create_engine(constants.DATABASE_URL, echo=True)

    # Bind the Base metadata to the engine
    Base.metadata.create_all(engine)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    db_count = session.query(Warning).count()

    # Add some dummy data
    dummy_user_type = Warning(title="fake title", description="description")
    session.add(dummy_user_type)
    session.commit()

    # Register a finalizer to clean up the data after the test
    def cleanup():
        session.query(Warning).filter_by(title="fake title").delete()
        session.commit()
        assert db_count == session.query(Warning).count()

    # Register cleanup to be executed after the test, even if it fails
    request.addfinalizer(cleanup)

    yield session  # Yield the session to the test

    # Cleanup manually after the test has finished (this could be redundant)
    session.close()


def test_get_warning_by_id(setup_database):
    # Get the session from the fixture
    session = setup_database

    # Fetch an existing material and update its data
    warning = session.query(Warning).filter_by(title="fake title").first()

    repository = WarningRepository(session)

    queried_warning = repository.get_warning_by_id(warning.id)

    assert warning.id == queried_warning.id


def test_create_warning(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = WarningRepository(session)

    warning = repository.create_warning("dummy", "word")
    queried_warning = repository.get_warning_by_id(warning.id)

    assert queried_warning is not None

    # Destroy
    session.query(Warning).filter_by(title="dummy").delete()
    session.commit()


def test_update_warning(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = WarningRepository(session)

    warning = repository.create_warning("dummy", "word")
    queried_warning = repository.get_warning_by_id(warning.id)

    repository.update_warning(queried_warning, new_title="dummy1", new_description=None)

    queried_warning = repository.get_warning_by_id(warning.id)

    assert queried_warning.title == "dummy1"

    # Destroy
    session.query(Warning).filter_by(title="dummy1").delete()
    session.commit()


def test_delete_warning(setup_database):
    # Get the session from the fixture
    session = setup_database
    repository = WarningRepository(session)

    warning = repository.create_warning("dummy", "word")
    queried_warning = repository.get_warning_by_id(warning.id)

    assert queried_warning is not None

    repository.delete_warning(queried_warning)

    queried_warning = repository.get_warning_by_id(warning.id)

    assert queried_warning is None

