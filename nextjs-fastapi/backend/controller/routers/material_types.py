import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.model.MaterialType import MaterialType
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from backend.controller.schemas.MaterialTypeUpdateRequest import MaterialTypeUpdateRequest
from backend.controller.schemas.MaterialTypeCreateRequest import MaterialTypeCreateRequest
from fastapi import FastAPI, Depends, HTTPException, Response, Request, APIRouter


router = APIRouter(
    prefix="/material_types",
    tags=["Material Types"],
)

@router.get("/")
async def get_all_material_types(db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)
    return repo.get_all_material_types()


@router.post("/create_mattype")
async def create_material_type(request: MaterialTypeCreateRequest, db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)

    type = db.query(MaterialType).filter_by(type_name=request.type_name).first()

    # Check if the entity exists
    if type is not None and repo.type_exists(type.id):
        raise HTTPException(status_code=404, detail="Material Type already exists")

    # Call the create method

    try:
        # Call the setter method to update the type
        repo.create_material_type(
            type_name=request.type_name
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material Type successfully created"}


@router.delete("/delete_mattype/{entity_id}")
async def delete_material_type(entity_id: int, db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)

    # Check if the entity exists
    if not repo.type_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material Type not found")

    # Call the update method
    type = repo.get_material_type_by_id(entity_id)

    try:
        # Call the setter method to update the type
        repo.delete_material_type(type)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material Type deleted successfully"}


@router.put("/update_mattype/{entity_id}")
async def update_material_type(entity_id: int, request: MaterialTypeUpdateRequest, db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)
    # Check if the entity exists
    if not repo.type_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material Type not found")

    # Call the update method
    type = repo.get_material_type_by_id(entity_id)
    try:
        # Call the setter method to update the user
        repo.update_material_type(type,
                                  type_name=request.type_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material Type updated successfully"}
