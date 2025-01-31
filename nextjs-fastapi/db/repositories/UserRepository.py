from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from db.model.User import User
from db.model.UserType import UserType


class UserRepository:
    def __init__(self, session: Session):
        """
        Constructor for the UserRepository.
        :param session: SQLAlchemy session to interact with the database
        """
        self.session = session

    def create_user(self, username: str, password: str, email: str, user_type_id: int) -> User:
        """
        Create a new User in the database.
        """
        try:
            # Create new User instance
            new_user = User(
                username=username,
                password=password,  # Assumes password is already hashed
                email=email,
                user_type_id=user_type_id
            )
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Integrity error: {e.orig}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a User by its ID.
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:

        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User:
        """
        Retrieve a User by its username.
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_all_users(self) -> list:
        """
        Retrieve all Users.
        """
        return self.session.query(User).all()

    def update_user(self, user: User, username: str = None, password: str = None, email: str = None,
                    user_type_id: int = None) -> User:
        """
        Update an existing User in the database.
        """
        try:
            if username:
                user.setUsername(username)
            if password:
                user.setHPass(password)
            if email:
                user.setEmail(email)
            if user_type_id:
                user.setUserTypeID(user_type_id)

            self.session.commit()
            return user
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def delete_user(self, user: User):
        """
        Delete a User from the database.
        """
        try:
            self.session.delete(user)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def user_exists(self, user_id: int):
        if self.get_user_by_id(user_id) is None:
            return False
        return True