import sys
from pathlib import Path

sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from db.repositories.UserRepository import UserRepository
from backend.controller import constants
from fastapi import FastAPI, Depends, HTTPException, Response, Request, APIRouter
import jwt
from datetime import datetime, timedelta
from typing import Optional
from backend.service.PasswordHashService import PasswordHashService


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
hash = PasswordHashService()


def decode_access_token(token: str):
    payload = jwt.decode(token, constants.SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def authenticate_user(username: str, password: str, db: Session):
    repo = UserRepository(db)
    user = repo.get_user_by_username(username)

    if hash.check_password(username, password, db):
        return user
    else:
        return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, constants.SECRET_KEY, algorithm=ALGORITHM)