from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.schemas.token_schema import Token
from app.db.session import get_db
from app.models.user_model import UserModel
from app.core.security import verify_password,create_access_token

auth_router=APIRouter(prefix="/auth",tags=['auth'])

@auth_router.post("/login",response_model=Token)
def login(email:str,password:str,db:Session=Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email==email).first()

    if not user or not verify_password(password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    access_token = create_access_token(
        data={
            "sub":str(user.id),
            "role":user.role
        }
    )

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }
