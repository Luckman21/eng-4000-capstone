import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from db.model.User import User
from db.model.UserType import UserType
from db.model.base import Base
from backend.service.PasswordHashService import PasswordHashService

# Fixture to setup an in-memory database for testing
@pytest.fixture(scope='module')
def session():
    # Setup the in-memory SQLite database engine
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # Create all tables defined in Base

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create sample UserType data for foreign key reference
    user_type = UserType(type_name='Admin')
    session.add(user_type)
    session.commit()

    yield session

    # Cleanup after test
    session.close()
    engine.dispose()

# Test case for User creation and initialization
def test_user_creation(session):
    user_type = session.query(UserType).first()  # Get the first UserType

    # Create a valid User
    user = User(
        username='testuser',
        password=PasswordHashService.hash_password('hashedpassword123'),
        email='testuser@example.com',
        user_type_id=user_type.id
    )
    
    session.add(user)
    session.commit()

    # Test that the user was successfully added
    assert user.id is not None
    assert user.username == 'testuser'
    assert user.password != 'hashedpassword123'
    assert PasswordHashService.verify_password(user.password, "hashedpassword123") is True
    assert user.email == 'testuser@example.com'
    assert user.user_type_id == user_type.id

# Test setUserTypeID method with valid and invalid inputs
def test_set_user_type_id(session):
    user_type = session.query(UserType).first()  # Get the first UserType
    another_user_type = UserType(type_name='User')
    session.add(another_user_type)
    session.commit()  # Commit to generate a new ID for the new user type

    user = User(
        username='testuser2',
        password='hashedpassword123',
        email='testuser2@example.com',
        user_type_id=user_type.id
    )

    # Update user's type
    user.setUserTypeID(another_user_type)
    assert user.user_type_id == another_user_type.id
    assert user.user_type == another_user_type

    # Invalid input: should raise ValueError if not passed a UserType instance
    with pytest.raises(ValueError):
        user.setUserTypeID('NonUserType')  # Passing an invalid type (string)

    # Rollback the session after the test
    session.rollback()

# Test setUserTypeID method with valid and invalid inputs
def test_set_user_type_id(session):
    user_type = session.query(UserType).first()  # Get the first UserType
    another_user_type = UserType(type_name='User')
    session.add(another_user_type)
    session.commit()  # Commit to generate a new ID for the new user type

    user = User(
        username='testuser2',
        password='hashedpassword123',
        email='testuser2@example.com',
        user_type_id=user_type.id
    )

    # Update user's type
    user.setUserTypeID(another_user_type.id)
    assert user.user_type_id == another_user_type.id

    # Invalid input: should raise ValueError if not passed a UserType instance
    with pytest.raises(ValueError):
        user.setUserTypeID('NonUserType')  # Passing an invalid type (string)

    # Rollback the session after the test
    session.rollback()

# Test getAll method for retrieving all users
def test_get_all_users(session):
    user_type = session.query(UserType).first()  # Get the first UserType

    user1 = User(
        username='user1',
        password='hashedpassword1',
        email='user1@example.com',
        user_type_id=user_type.id
    )
    
    user2 = User(
        username='user2',
        password='hashedpassword2',
        email='user2@example.com',
        user_type_id=user_type.id
    )
    
    session.add(user1)
    session.add(user2)
    session.commit()

    # Test the getAll method to fetch all users
    users = User.getAll(User, session)
    assert len(users) == 3  # We added two users, plus the first user from test1, testuser
    assert users[0].username == 'testuser'
    assert users[1].username == 'user1'
    assert users[2].username == 'user2'

    # Rollback the session after the test
    session.rollback()
