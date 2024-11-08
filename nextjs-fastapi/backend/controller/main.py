from fastapi import FastAPI
from typing import Union
import sqlite3





app = FastAPI()


# Now define your API routes

@app.get("/materials")
async def get_Allmaterials():
    conn = sqlite3.connect('../../db/capstone_db.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()
    conn.close()

    return {"materials": materials}

@app.get("/materials/{material_type}")
async def get_materials(material_type: str):
    conn = sqlite3.connect('../../db/capstone_db.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM material WHERE material_type = ?", (material_type,))
    materials = cursor.fetchall()
    conn.close()

    return {"materials": materials}
