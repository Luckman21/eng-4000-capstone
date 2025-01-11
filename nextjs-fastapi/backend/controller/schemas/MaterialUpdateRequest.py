# app/schemas.py (or wherever you store Pydantic models)
from pydantic import BaseModel
from typing import Optional


class MaterialUpdateRequest(BaseModel):
    colour: Optional[str] = None
    name: Optional[str] = None
    mass: Optional[float] = None
    material_type_id: Optional[int] = None

# app/schemas.py (or wherever you store Pydantic models)
from pydantic import BaseModel
from typing import Optional


class MaterialUpdateRequest(BaseModel):
    colour: Optional[str] = None
    name: Optional[str] = None
    mass: Optional[float] = None
    material_type_id: Optional[int] = None