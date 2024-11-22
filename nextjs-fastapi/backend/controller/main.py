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

# Now define your API routes
@app.get("/materials", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    return repo.get_all_materials()

# @app.get("/materials/{material_type}")

if __name__ == "__main__":
    db: Session = Depends(get_db)
    repo = MaterialRepository(db)
    event.listen(repo, 'after_update', listener.job_complete_listener)