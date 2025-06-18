import sys
from pathlib import Path

sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.schemas import MaterialSchema
from backend.controller.schemas.MaterialUpdateRequest import MaterialUpdateRequest
from backend.controller.schemas.MaterialCreateRequest import MaterialCreateRequest
from backend.controller.schemas.MaterialMutationRequest import MaterialMutationRequest
from fastapi import Depends, HTTPException, APIRouter
from backend.service.controller_service import material_service

router = APIRouter(
    prefix="/materials",
    tags=["Materials"],
)


# Now define your API routes
@router.get("/", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    materials = material_service.get_all_materials(db)

    return materials


@router.post("/create_material")
async def create_material(request: MaterialCreateRequest, db: Session = Depends(get_db)):
    exists = material_service.check_material_existance(db, supplier_link=request.supplier_link, colour=request.colour,
                                                       material_type_id=request.material_type_id)

    if exists:
        raise HTTPException(status_code=404, detail="Material already exists")

    try:
        material_service.create_material(
            db,
            colour=request.colour,
            supplier_link=request.supplier_link,
            mass=request.mass,
            material_type_id=request.material_type_id,
            shelf_id=request.shelf_id
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material successfully created"}


@router.delete("/delete_material/{entity_id}")
async def delete_material(entity_id: int, db: Session = Depends(get_db)):
    exists = material_service.check_material_existance(db, entity_id=entity_id)

    if not exists:
        raise HTTPException(status_code=404, detail="Material not found")

    try:
        material_service.delete_material(db, entity_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material deleted successfully"}


@router.patch("/replenish_mass/{entity_id}")
async def replenish_mass(entity_id: int, request: MaterialMutationRequest, db: Session = Depends(get_db)):
    exists = material_service.check_material_existance(db, entity_id=entity_id)

    if not exists:
        raise HTTPException(status_code=404, detail="Material not found")

    try:
        material_service.replenish_mass(db, entity_id, request.mass_change)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': f"{request.mass_change} grams replenished"}


@router.patch("/consume_mass/{entity_id}")
async def consume_mass(entity_id: int, request: MaterialMutationRequest, db: Session = Depends(get_db)):
    exists = material_service.check_material_existance(db, entity_id=entity_id)

    if not exists:
        raise HTTPException(status_code=404, detail="Material not found")

    try:
        material_service.consume_mass(db, entity_id, request.mass_change)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': f"{request.mass_change} grams consumed"}


@router.put("/update_material/{entity_id}")
async def update_material(entity_id: int, request: MaterialUpdateRequest, db: Session = Depends(get_db)):
    exists = material_service.check_material_existance(db, entity_id=entity_id)

    if not exists:
        raise HTTPException(status_code=404, detail="Material not found")

    try:
        material_service.update_material(
            db,
            entity_id=entity_id,
            mass=request.mass,
            colour=request.colour,
            material_type_id=request.material_type_id,
            supplier_link=request.supplier_link,
            shelf_id=request.shelf_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material updated successfully"}
