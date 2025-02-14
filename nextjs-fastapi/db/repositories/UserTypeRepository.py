from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from db.model.UserType import UserType

class UserTypeRepository:
    def __init__(self, session: Session):
        """
        Constructor for UserTypeRepository.
        :param session: SQLAlchemy session to interact with the database
        """
        self.session = session

    def create_user_type(self, type_name: str) -> UserType:
        """
        Create a new UserType in the database.
        """
        try:
            # Create new UserType instance
            new_user_type = UserType(type_name=type_name)
            self.session.add(new_user_type)
            self.session.commit()
            return new_user_type
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Integrity error: {e.orig}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def get_user_type_by_id(self, user_type_id: int) -> UserType:
        """
        Retrieve a UserType by its ID.
        """
        return self.session.query(UserType).filter(UserType.id == user_type_id).first()

    def get_user_type_by_name(self, type_name: str) -> UserType:
        """
        Retrieve a UserType by its name.
        """
        return self.session.query(UserType).filter(UserType.type_name == type_name).first()

    def get_all_user_types(self) -> list:
        """
        Retrieve all UserTypes from the database.
        """
        return self.session.query(UserType).order_by(UserType.id).all()

    def update_user_type(self, user_type: UserType, new_type_name: str) -> UserType:
        """
        Update an existing UserType's name.
        """
        try:
            user_type.setName(new_type_name)
            self.session.commit()
            return user_type
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def delete_user_type(self, user_type: UserType):
        """
        Delete a UserType from the database.
        """
        try:
            self.session.delete(user_type)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")
