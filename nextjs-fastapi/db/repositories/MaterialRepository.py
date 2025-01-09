from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from sqlalchemy.orm import Session
from db.model.Material import Material
from db.model.MaterialType import MaterialType


class MaterialRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_material(self, colour: str, name: str, mass: float, material_type_id: int, shelf_id: int) -> Material:
        """
        Create a new Material record in the database.
        """
        try:
            new_material = Material(
                colour=colour,
                name=name,
                mass=mass,
                material_type_id=material_type_id,
                shelf_id=shelf_id
            )
            self.session.add(new_material)
            self.session.commit()
            return new_material
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Integrity error: {e.orig}")
        except DataError as e:
            self.session.rollback()
            raise ValueError(f"Data error: {e.orig}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def get_material_by_id(self, material_id: int) -> Material:
        """
        Retrieve a material by its ID.
        """
        return self.session.query(Material).filter(Material.id == material_id).first()

    def get_all_materials(self) -> list:
        """
        Retrieve all materials from the database.
        """
        return self.session.query(Material).all()

    def update_material(self, material: Material, colour: str = None, name: str = None, mass: float = None,
                        material_type_id: int = None, shelf_id: int = None ) -> Material:
        """
        Update an existing material.
        """
        try:
            if colour:
                material.setColour(colour)
            if name:
                material.setName(name)
            if mass is not None:
                material.mass = mass
            if material_type_id:
                material.setMaterialTypeID(material_type_id)
            if shelf_id is not None:
                material.shelf_id = shelf_id

            self.session.commit()
            return material
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def delete_material(self, material: Material):
        """
        Delete a material from the database.
        """
        try:
            self.session.delete(material)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")
