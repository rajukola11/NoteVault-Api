from fastapi import HTTPException,Depends,status
import os
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from datetime import datetime,timezone

from app.db.session import get_db
from app.models.user_model import UserModel
from app.schemas.token_schema import TokenPayload


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM ="HS256"


def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:Session = Depends(get_db)
)->UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        token_data=TokenPayload(**payload)
    except JWTError:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.id == token_data.sub).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive or deleted user"
        )
    
    return user
