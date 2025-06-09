from pydantic import BaseModel
from typing import Optional


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    user_type_id: Optional[int] = None