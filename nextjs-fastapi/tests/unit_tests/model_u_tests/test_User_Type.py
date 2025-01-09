import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from db.model.UserType import UserType
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

# Test case for UserType creation and initialization
def test_user_type_creation(session):
    # Create a valid UserType
    user_type = UserType(type_name='Admin')
    session.add(user_type)
    
    session.commit()

    # Test that the UserType was successfully added
    assert user_type.id is not None
    assert user_type.type_name == 'Admin'

    # Rollback the session after the test
    session.rollback()

'''
# Test invalid type_name (non-string value) raises ValueError
def test_user_type_invalid_name(session):
    user_type = UserType(type_name=123)  # Invalid type_name (non-string value)
    
    session.add(user_type)

    # Check for IntegrityError due to invalid type_name (if you want to enforce only strings)
    with pytest.raises(ValueError):
        session.commit()

    # Rollback the session after the test
    session.rollback()
'''

'''
# Test setName method with valid and invalid inputs
def test_set_name(session):
    user_type = UserType(type_name='Admin')
    session.add(user_type)
    session.commit()
    
    # Update name
    user_type.setName('User')
    assert user_type.type_name == 'User'

    # Invalid input: name must be a string
    with pytest.raises(ValueError):
        user_type.setName(123)  # Passing an integer instead of a string

    # Rollback the session after the test
    session.rollback()
'''

# Test getAll method for retrieving all user types
def test_get_all_user_types(session):
    user_type1 = UserType(type_name='Admin')
    user_type2 = UserType(type_name='User')
    session.add(user_type1)
    session.rollback()
    session.add(user_type2)

    session.commit()

    # Test the getAll method to fetch all user types
    user_types = UserType.getAll(UserType, session)
    assert len(user_types) == 2  # We added two user types
    assert user_types[0].type_name == 'Admin'
    assert user_types[1].type_name == 'User'

    # Rollback the session after the test
    session.rollback()

'''
# Test invalid input types (type_name must be string)
def test_invalid_input_types(session):
    with pytest.raises(TypeError):
        UserType(type_name=123)  # type_name should be a string

    # Rollback the session after the test
    session.rollback()
'''