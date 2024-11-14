import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from fastapi import FastAPI, Depends
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from dependencies import get_db
from db.schemas import MaterialSchema 
from db.model.Material import Material
from db.scripts.DatabasePopulate import populate_db
from fastapi.middleware.cors import CORSMiddleware

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
    return Material.getAll(Material,db)


# @app.get("/materials/{material_type}")
