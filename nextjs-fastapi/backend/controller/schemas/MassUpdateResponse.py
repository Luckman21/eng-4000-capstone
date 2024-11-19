# app/schemas.py (or wherever you store Pydantic models)
from pydantic import BaseModel


class MassUpdateResponse(BaseModel):
    message: str
    new_mass: float
