import sys
from pathlib import Path

import uvicorn
sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.repositories.UserRepository import UserRepository
from backend.controller import constants
from fastapi import FastAPI, Depends, HTTPException, Response, Request, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from backend.service.PasswordHashService import PasswordHashService
from datetime import datetime, timedelta
from typing import Optional
from backend.service.mailer.TempPasswordMailer import TempPasswordMailer
from backend.service.TempPasswordRandomizeService import create_temp_password
from backend.controller.schemas.ForgotPasswordRequest import ForgotPasswordRequest
from backend.service.controller_service import access_service

router = APIRouter(
    prefix="/access_management",
    tags=["Access"],
)


ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = access_service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create JWT access token
    access_token = access_service.create_access_token(
        data={"username": user.username, "user_type_id": user.user_type_id, "email": user.email, "id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )

    return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response):
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return {"message": "Logged out successfully"}


@router.get("/protected")
def protected_route(request: Request, response: Response):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = access_service.decode_access_token(token)
        # Generate a new token with an updated expiration time
        new_token = access_service.create_access_token(
            data={"username": payload["username"], "user_type_id": payload["user_type_id"], "email": payload["email"],
                  "id": payload["id"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),  # Reset expiration
        )

        # Update the cookie with the new token
        response.set_cookie(
            key="access_token",
            value=new_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )

        return {"message": "Access granted", "user": payload}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/forgot_password/")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    # Check if the entity exists
    if not repo.user_email_exists(request.email):
        raise HTTPException(status_code=404, detail="User not found")

    user = repo.get_user_by_email(request.email)

    # Create password, update, and send

    plain_password = create_temp_password()
    hashed_password = PasswordHashService.hash_password(plain_password)

    try:
        # Call the setter method to update the user

        repo.update_user(user,
                         password=hashed_password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        mailer = TempPasswordMailer(from_addr=constants.MAILER_EMAIL)
        mailer.send_notification(user.email, plain_password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'message': "Password successfully sent"}


