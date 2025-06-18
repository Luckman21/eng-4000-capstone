import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from backend.controller.schemas.MaterialTypeUpdateRequest import MaterialTypeUpdateRequest
from backend.controller.schemas.MaterialTypeCreateRequest import MaterialTypeCreateRequest
from fastapi import Depends, HTTPException, APIRouter
from backend.service.controller_service import material_type_service

router = APIRouter(
    prefix="/material_types",
    tags=["Material Types"],
)


@router.get("/")
async def get_all_material_types(db: Session = Depends(get_db)):
    material_types = material_type_service.get_all_material_types(db)

    return material_types


@router.post("/create_mattype")
async def create_material_type(request: MaterialTypeCreateRequest, db: Session = Depends(get_db)):

    exists = material_type_service.check_material_type_existance(db, type_name=request.type_name)

    if exists:
        raise HTTPException(status_code=404, detail="Material Type already exists")

    try:
        material_type_service.create_material_type(db, request.type_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material Type successfully created"}


@router.delete("/delete_mattype/{entity_id}")
async def delete_material_type(entity_id: int, db: Session = Depends(get_db)):

    exists = material_type_service.check_material_type_existance(db, entity_id=entity_id)

    if not exists:
        raise HTTPException(status_code=404, detail="Material Type not found")

    try:
        material_type_service.delete_material_type(db, entity_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material Type deleted successfully"}


@router.put("/update_mattype/{entity_id}")
async def update_material_type(entity_id: int, request: MaterialTypeUpdateRequest, db: Session = Depends(get_db)):
    exists = material_type_service.check_material_type_existance(db, entity_id=entity_id)

    if not exists:
        raise HTTPException(status_code=404, detail="Material Type not found")

    try:
        material_type_service.update_material_type(db, entity_id, request.type_name)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material Type updated successfully"}
