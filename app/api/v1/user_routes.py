from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user_schema import UserCreate,UserRead
from app.models.user_model import UserModel
from app.db.session import get_db
from app.core.security import hash_password

user_router = APIRouter()

@user_router.post("/users",status_code=status.HTTP_201_CREATED,response_model=UserRead)
def create_a_user(user_data:UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email==user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    new_user=UserModel(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user_router.get("/users/{user_id}",response_model=UserRead)
def get_a_user(user_id:int,db:Session=Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@user_router.get("/users",response_model=List[UserRead])
def get_all_user(db:Session=Depends(get_db)):
    all_users=db.query(UserModel).all()
    return all_users
