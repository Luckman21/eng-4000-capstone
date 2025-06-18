import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.repositories.MaterialRepository import MaterialRepository
from backend.service.listener.EmbeddedListener import get_scale_listener
from fastapi import Depends, HTTPException, APIRouter

router = APIRouter(
    prefix="/qr_display",
    tags=["qr"],
)


@router.get("/{entity_id}")
async def auto_consume_mass(entity_id: int, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    material = repo.get_material_by_id(entity_id)

    mass_on_the_scale = get_mass_from_scale()
    material_type_name = material.material_type.type_name
    
    if mass_on_the_scale == None:
        raise HTTPException(status_code=500, detail="No mass reading has been updated yet")
    if mass_on_the_scale <= 0.0:
        raise HTTPException(status_code=500, detail="Mass reading on scale is less than or equal to zero")

    return {'mass': mass_on_the_scale, 'material': material, 'material_type_name': material_type_name}


def get_mass_from_scale():
    """Retrieves latest mass value stored."""
    scale_mqtt_instance = get_scale_listener()
    return scale_mqtt_instance.get_latest_value()