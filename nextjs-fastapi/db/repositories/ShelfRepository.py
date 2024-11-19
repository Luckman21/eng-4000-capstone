from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from db.model.Shelf import Shelf

class ShelfRepository:
    def __init__(self, session: Session):
        """
        Constructor for ShelfRepository.
        :param session: SQLAlchemy session to interact with the database
        """
        self.session = session

    def create_shelf(self, humidity_pct: float, temperature_cel: float) -> Shelf:
        """
        Create a new Shelf in the database.
        """
        try:
            new_shelf = Shelf(humidity_pct=humidity_pct, temperature_cel=temperature_cel)
            self.session.add(new_shelf)
            self.session.commit()
            return new_shelf
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Integrity error: {e.orig}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def get_shelf_by_id(self, shelf_id: int) -> Shelf:
        """
        Retrieve a Shelf by its ID.
        """
        return self.session.query(Shelf).filter(Shelf.id == shelf_id).first()

    def get_all_shelves(self) -> list:
        """
        Retrieve all Shelves from the database.
        """
        return self.session.query(Shelf).all()

    def update_shelf(self, shelf: Shelf, new_humidity_pct: float, new_temperature_cel: float) -> Shelf:
        """
        Update an existing Shelf's humidity and temperature.
        """
        try:
            shelf.humidity_pct = new_humidity_pct
            shelf.temperature_cel = new_temperature_cel
            self.session.commit()
            return shelf
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def delete_shelf(self, shelf: Shelf):
        """
        Delete a Shelf from the database.
        """
        try:
            self.session.delete(shelf)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")
