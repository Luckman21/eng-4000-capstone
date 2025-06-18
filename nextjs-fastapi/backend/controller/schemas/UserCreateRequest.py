from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str
    user_type_id: int