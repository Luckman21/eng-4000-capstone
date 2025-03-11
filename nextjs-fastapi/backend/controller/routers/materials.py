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
    prefix="/materials",
    tags=["Materials"],
)


# Now define your API routes
@router.get("/", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    return repo.get_all_materials()


@router.post("/create_material")
async def create_material(request: MaterialCreateRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    material = db.query(Material).filter_by(supplier_link=request.supplier_link, colour=request.colour,
                                            material_type_id=request.material_type_id).first()

    # Check if the entity exists
    if material is not None and repo.material_exists(material.id):
        raise HTTPException(status_code=404, detail="Material already exists")

    # Call the update method

    try:
        # Call the setter method to update the material
        repo.create_material(
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
    repo = MaterialRepository(db)

    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)

    try:
        # Call the setter method to update the material
        repo.delete_material(material)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    material = repo.get_material_by_id(entity_id)

    return {'message': "Material deleted successfully"}


@router.patch("/replenish_mass/{entity_id}")
async def replenish_mass(entity_id: int, request: MaterialMutationRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    # Check if the entity exists

    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)
    try:
        # Call the setter method to update the material
        repo.update_material(material,
                             mass=(material.mass + request.mass_change),
                             colour=None,
                             material_type_id=None,
                             supplier_link=None,
                             shelf_id=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': f"{request.mass_change} grams replenished"}


@router.patch("/consume_mass/{entity_id}")
async def consume_mass(entity_id: int, request: MaterialMutationRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)

    # Check mass diference

    if request.mass_change > material.mass:
        raise HTTPException(status_code=400, detail="Consumed mass greater than material's mass")
    try:
        # Call the setter method to update the material
        repo.update_material(material,
                             mass=(material.mass - request.mass_change),
                             colour=None,
                             material_type_id=None,
                             supplier_link=None,
                             shelf_id=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': f"{request.mass_change} grams consumed"}


@router.put("/update_material/{entity_id}")
async def update_material(entity_id: int, request: MaterialUpdateRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)
    try:
        # Call the setter method to update the material
        repo.update_material(material,
                             mass=request.mass,
                             colour=request.colour,
                             material_type_id=request.material_type_id,
                             supplier_link=request.supplier_link,
                             shelf_id=request.shelf_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material updated successfully"}

