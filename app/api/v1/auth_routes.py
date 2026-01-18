from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token_schema import Token
from app.db.session import get_db
from app.models.user_model import UserModel
from app.core.security import verify_password,create_access_token
from app.core.errors import unauthorized,forbidden

auth_router=APIRouter(prefix="/auth",tags=['auth'])

@auth_router.post("/login",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email==form_data.username).first()

    if not user or not verify_password(form_data.password,user.hashed_password):
        unauthorized()
    if not user.is_active:
        forbidden("Inactive user")

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
