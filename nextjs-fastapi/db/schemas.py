from pydantic import BaseModel

class MaterialSchema(BaseModel):
    id: int
    colour: str
    name: str
    mass: float
    material_type_id: int
    shelf_id: int

    class Config:
        orm_mode = True
