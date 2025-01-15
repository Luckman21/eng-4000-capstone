import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.schemas import MaterialSchema 
from db.model.Material import Material
from fastapi.middleware.cors import CORSMiddleware
from db.repositories.MaterialRepository import MaterialRepository
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from backend.controller.schemas.MassUpdateRequest import MassUpdateRequest
from backend.controller.schemas.MaterialUpdateRequest import MaterialUpdateRequest
from backend.controller.schemas.MaterialCreateRequest import MaterialCreateRequest
from pydantic import BaseModel
import asyncio
from sqlalchemy import event
from backend.controller import listener
from backend.controller.schemas.MassUpdateRequest import MassUpdateRequest
from backend.controller.schemas.MaterialUpdateRequest import MaterialUpdateRequest
from backend.controller.schemas.MaterialCreateRequest import MaterialCreateRequest
from db.repositories.MaterialTypeRepository import MaterialTypeRepository

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up listeners on startup
@app.on_event("startup")
def setup_listeners():
    low_stock_listener()

# Create a listener that triggers when the Material table is updated, checks for Materials with a mass below the threshold
def low_stock_listener():
    def listener_wrapper(mapper, connection, target):
        asyncio.create_task(listener.job_complete_listener(mapper, connection, target))

    event.listen(Material, 'after_update', listener_wrapper)

# Now define your API routes
@app.get("/materials", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    return repo.get_all_materials()

@app.get("/material_types")
async def get_all_material_types(db: Session = Depends(get_db)):
    repo =MaterialTypeRepository(db)
    return repo.get_all_material_types()




@app.put("/update_mass/{entity_id}")
async def update_mass(entity_id: int, request: MassUpdateRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Mass entity not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)

    try:
        # Call the setter method to update the mass
        repo.update_material(material, mass=request.mass)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    material = repo.get_material_by_id(entity_id)

    return {'message': "Mass updated successfully", 'new_mass' : material.mass}

@app.post("/create_material")
async def create_material(request: MaterialCreateRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    material = db.query(Material).filter_by(name=request.name, colour=request.colour, material_type_id=request.material_type_id).first()

    # Check if the entity exists
    if material is not None and repo.material_exists(material.id):
        raise HTTPException(status_code=404, detail="Material already exists")

    # Call the update method

    try:
        # Call the setter method to update the material
        repo.create_material( 
                             colour=request.colour,
                             name=request.name,
                             mass=request.mass,
                             material_type_id=request.material_type_id,
                             shelf_id=request.shelf_id
                             )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material successfully created"}

@app.get("/material_types")
async def get_all_material_types(db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)
    return repo.get_all_material_types()


@app.delete("/delete_material/{entity_id}")
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

@app.put("/update_material/{entity_id}")
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
                             name=request.name,
                             shelf_id = request.shelf_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material updated successfully"}

def get_app():
    return app