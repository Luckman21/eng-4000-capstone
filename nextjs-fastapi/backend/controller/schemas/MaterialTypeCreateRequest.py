# app/schemas.py (or wherever you store Pydantic models)
from pydantic import BaseModel
from typing import Optional


class MaterialTypeCreateRequest(BaseModel):
    type_name: str