from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from db.model.Warning import Warning


class WarningRepository:
    def __init__(self, session: Session):
        """
        Constructor for WarningRepository.
        :param session: SQLAlchemy session to interact with the database
        """
        self.session = session

    def create_warning(self, title: str, description: str) -> Warning:
        """
        Create a new Warning in the database.
        """
        try:
            new_warning = Warning(title=title, description=description)
            self.session.add(new_warning)
            self.session.commit()
            return new_warning
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Integrity error: {e.orig}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def get_warning_by_id(self, warning_id: int) -> Warning:
        """
        Retrieve a Warning by its ID.
        """
        return self.session.query(Warning).filter(Warning.id == warning_id).first()

    def get_all_warnings(self) -> list:
        """
        Retrieve all Warnings from the database.
        """
        return self.session.query(Warning).order_by(Warning.id).all()

    def update_warning(self, warning: Warning, new_title: str = None, new_description: str = None) -> Warning:
        """
        Update an existing Warning's title and description.
        """
        try:
            if new_title:
                warning.setTitle(new_title)
            if new_description:
                warning.setDescription(new_description)
            self.session.commit()
            return warning
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def delete_warning(self, warning: Warning):
        """
        Delete a Warning from the database.
        """
        try:
            self.session.delete(warning)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")