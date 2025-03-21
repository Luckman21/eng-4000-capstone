import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from db.model.MaterialType import MaterialType
from db.repositories.MaterialTypeRepository import MaterialTypeRepository

def get_all_material_types(db):
    repo = MaterialTypeRepository(db)
    return repo.get_all_material_types()


def create_material_type(db, type_name):
    repo = MaterialTypeRepository(db)

    # Call the setter method to update the type
    repo.create_material_type(
        type_name=type_name
    )
    return None


def delete_material_type(db, entity_id):
    repo = MaterialTypeRepository(db)

    type = repo.get_material_type_by_id(entity_id)

    repo.delete_material_type(type)

def update_material_type(db, entity_id, new_type_name):
    repo = MaterialTypeRepository(db)
    type = repo.get_material_type_by_id(entity_id)

    repo.update_material_type(type,
                              type_name=new_type_name)


def check_material_type_existance(db, type_name: str = None, entity_id: int = None):
    repo = MaterialTypeRepository(db)

    type = db.query(MaterialType).filter_by(type_name=type_name).first()

    # Check if the entity exists
    if type is not None and repo.type_exists(type.id):
        return True
    elif type is None and repo.type_exists(entity_id):
        return True

    return False