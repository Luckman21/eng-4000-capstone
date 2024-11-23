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
# from backend.controller.schemas import MassUpdateRequest, MassUpdateResponse
from pydantic import BaseModel
import asyncio
from sqlalchemy import event
from controller import listener
class MassUpdateRequest(BaseModel):
    mass: float

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

# Register listener to trigger after an insert to Material
@event.listens_for(Material, "after_update")
def low_inventory_listener(mapper, connection, target):
    print(f"Low inventory listener triggered for {target.name}!")

    sess = connection._session
    repo = MaterialRepository(sess)

    print("still running")
    asyncio.create_task(listener.job_complete_listener(repo)) 

# Now define your API routes
@app.get("/materials", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    return repo.get_all_materials()

# @app.get("/materials/{material_type}")

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

def get_app():
    return app