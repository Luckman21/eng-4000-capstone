import sys
from pathlib import Path

sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.schemas import MaterialSchema
from db.model.Material import Material
from db.repositories.MaterialRepository import MaterialRepository
from backend.controller.schemas.MaterialUpdateRequest import MaterialUpdateRequest
from backend.controller.schemas.MaterialCreateRequest import MaterialCreateRequest
from backend.controller.schemas.MaterialMutationRequest import MaterialMutationRequest
from fastapi import FastAPI, Depends, HTTPException, Response, Request, APIRouter


router = APIRouter(
    prefix="/qr_display",
    tags=["qr"],
)



@router.get("/{entity_id}")
async def auto_consume_mass(entity_id: int, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)

    mass_on_the_scale = get_mass_from_scale()  # TODO add listener call
    material_type_name = material.material_type.type_name

    if mass_on_the_scale <= 0.0:
        raise HTTPException(status_code=500, detail="Mass reading on scale is less than or equal to zero")

    return {'mass': mass_on_the_scale, 'material': material, 'material_type_name': material_type_name}


def get_mass_from_scale():
    """Simulates retrieving mass from the embedded system (to be replaced later)."""
    return 2.0  # Placeholder for now