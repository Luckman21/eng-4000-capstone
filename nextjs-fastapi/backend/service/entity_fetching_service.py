from db.schemas import MaterialSchema
from db.model.Material import Material
from db.repositories.MaterialRepository import MaterialRepository

class EntityFetchingService:

    def get_all_materials(self, db):
        repo = MaterialRepository(db)
        return repo.get_all_materials()
