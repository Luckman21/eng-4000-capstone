from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from db.model.Shelf import Shelf
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

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
        return self.session.query(Shelf).order_by(Shelf.id).all()

    def update_shelf(self, shelf: Shelf, new_humidity_pct: float = None, new_temperature_cel: float = None) -> Shelf:
        """
        Update an existing Shelf's humidity and temperature.
        """
        try:
            if new_humidity_pct:
                shelf.humidity_pct = new_humidity_pct
            if new_temperature_cel:
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

    async def get_high_humidity_shelves_async(self):
        """
        Return shelves with humidity above threshold.
        """
        result = await self.session.execute(
            select(Shelf).where(Shelf.humidity_pct > 20)
        )
        return result.scalars().all()

    async def get_high_temperature_shelves_async(self):
        """
        Return shelves with temperature above threshold.
        """
        result = await self.session.execute(
            select(Shelf).where(Shelf.temperature_cel > 30)
        )
        return result.scalars().all()
