import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from db.model.Material import Material
from db.repositories.MaterialRepository import MaterialRepository

def get_all_materials(db):
    repo = MaterialRepository(db)
    return repo.get_all_materials()


def create_material(db, colour: str = None, supplier_link: str = None, mass: float = None, material_type_id: int = None, shelf_id: int = None):
    repo = MaterialRepository(db)

    # Call the setter method to update the type
    repo.create_material(
        colour=colour,
        supplier_link=supplier_link,
        mass=mass,
        material_type_id=material_type_id,
        shelf_id=shelf_id
    )
    return None


def delete_material(db, entity_id):
    repo = MaterialRepository(db)

    material = repo.get_material_by_id(entity_id)

    repo.delete_material(material)


def update_material(db, entity_id, colour: str = None, supplier_link: str = None, mass: float = None, material_type_id: int = None, shelf_id: int = None ):
    repo = MaterialRepository(db)
    material = repo.get_material_by_id(entity_id)

    repo.update_material(material,
                         mass=mass,
                         colour=colour,
                         material_type_id=material_type_id,
                         supplier_link=supplier_link,
                         shelf_id=shelf_id)


def consume_mass(db, entity_id, consumed_mass):

    repo = MaterialRepository(db)
    material = repo.get_material_by_id(entity_id)

    if consumed_mass > material.mass:
        raise Exception("Consumed mass greater than material's mass")

    repo.update_material(material,
                         mass=(material.mass-consumed_mass),
                         colour=None,
                         material_type_id=None,
                         supplier_link=None,
                         shelf_id=None)


def replenish_mass(db, entity_id, replenished_mass):
    repo = MaterialRepository(db)
    material = repo.get_material_by_id(entity_id)

    repo.update_material(material,
                         mass=(material.mass + replenished_mass),
                         colour=None,
                         material_type_id=None,
                         supplier_link=None,
                         shelf_id=None)


def check_material_existance(db, supplier_link: str = None, colour: str = None, material_type_id: int = None, entity_id: int = None):
    repo = MaterialRepository(db)

    material = db.query(Material).filter_by(supplier_link=supplier_link, colour=colour,
                                            material_type_id=material_type_id).first()

    # Check if the entity exists
    if material is not None and repo.material_exists(material.id):
        return True
    elif material is None and repo.material_exists(entity_id):
        return True

    return False