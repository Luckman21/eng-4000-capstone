# app/schemas.py (or wherever you store Pydantic models)
from pydantic import BaseModel
from typing import Optional


class MaterialTypeUpdateRequest(BaseModel):
    type_name: Optional[str] = None
