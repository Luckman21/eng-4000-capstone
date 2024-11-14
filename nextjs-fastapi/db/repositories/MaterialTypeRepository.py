from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from sqlalchemy.orm import Session
from db.model.Material import Material
from db.model.Material_Type import MaterialType


class MaterialTypeRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_material_type(self, type_name: str ) -> MaterialType:
        """
        Create a new MaterialType record in the database.
        """
        try:
            new_material_type = MaterialType(
             type_name=type_name
            )
            self.session.add(new_material_type)
            self.session.commit()
            return new_material_type
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

    def get_material_by_id(self, material_type_id: int) -> MaterialType:
        """
        Retrieve a material_type by its ID.
        """
        return self.session.query(MaterialType).filter(MaterialType.id == material_type_id).first()

    def get_all_material_types(self) -> list:
        """
        Retrieve all materials from the database.
        """
        return self.session.query(MaterialType).all()

    def update_material_type(self, material_type: MaterialType, type_name: str ) -> MaterialType:
        """
        Update an existing material type.
        """
        try:
            if type_name:
                material_type.setName(type_name)

            self.session.commit()
            return material_type
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")

    def delete_material_type(self, material_type: MaterialType):
        """
        Delete a material type from the database.
        """
        try:
            self.session.delete(material_type)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Unexpected error: {e}")
