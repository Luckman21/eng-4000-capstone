# app/schemas.py (or wherever you store Pydantic models)
from pydantic import BaseModel
from typing import Optional


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str
    user_type_id: int