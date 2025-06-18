import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.model.User import User
from db.repositories.UserRepository import UserRepository
from backend.controller import constants
from backend.controller.schemas.UserUpdateRequest import UserUpdateRequest
from backend.controller.schemas.UserCreateRequest import UserCreateRequest
from fastapi import Depends, HTTPException, APIRouter
from backend.service.mailer.PasswordChangeMailer import PasswordChangeMailer
from backend.service.PasswordHashService import PasswordHashService
from backend.service.controller_service import access_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/all_users")
async def get_all_users(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return repo.get_all_users()


@router.post("/create_user")
async def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    user = db.query(User).filter_by(email=request.email, username=request.username,
                                    user_type_id=request.user_type_id).first()

    if user is not None and repo.user_exists(user.id):
        raise HTTPException(status_code=404, detail="User already exists")

    try:
        repo.create_user(
            username=request.username,
            user_type_id=request.user_type_id,
            password=PasswordHashService.hash_password(request.password),
            email=request.email
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "User successfully created"}


@router.delete("/delete_user/{entity_id}")
async def delete_user(entity_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    if not repo.user_exists(entity_id):
        raise HTTPException(status_code=404, detail="User not found")

    user = repo.get_user_by_id(entity_id)

    try:
        repo.delete_user(user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "User deleted successfully"}


@router.put("/update_user/{entity_id}")
async def update_user(entity_id: int, request: UserUpdateRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    if not repo.user_exists(entity_id):
        raise HTTPException(status_code=404, detail="User not found")

    user = repo.get_user_by_id(entity_id)

    try:
        password = None
        if request.password is not None:
            password = PasswordHashService.hash_password(request.password)

        repo.update_user(user,
                         username=request.username,
                         password=password,
                         email=request.email,
                         user_type_id=request.user_type_id
                         )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        if request.password is not None:
            mailer = PasswordChangeMailer(from_addr=constants.MAILER_EMAIL)
            mailer.send_notification(user.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_token = access_service.create_access_token(data={
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "user_type_id": user.user_type_id,
    })

    return {'message': "User updated successfully", "access_token": new_token}
