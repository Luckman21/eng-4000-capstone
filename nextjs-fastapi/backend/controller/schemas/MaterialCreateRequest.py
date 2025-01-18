# app/schemas.py (or wherever you store Pydantic models)
from pydantic import BaseModel
from typing import Optional


class MaterialCreateRequest(BaseModel):
    colour: str
    supplier_link: str
    mass: float
    material_type_id: int
    shelf_id: Optional[int] = None