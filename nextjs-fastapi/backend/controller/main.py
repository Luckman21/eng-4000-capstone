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










app = FastAPI()


# Now define your API routes
@app.get("/materials", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    return Material.getAll(Material,db)
    


# @app.get("/materials/{material_type}")
# async def get_materials(material_type: str):
#     conn = sqlite3.connect('../../db/capstone_db.db')
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM material WHERE material_type = ?", (material_type,))
#     materials = cursor.fetchall()
#     conn.close()

#     return {"materials": materials}
