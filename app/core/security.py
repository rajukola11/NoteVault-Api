from passlib.context import CryptContext
from datetime import timedelta,datetime,timezone
import os
from jose import jwt

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment variables")

pwd_context = CryptContext(
    schemes = ["argon2"],
    deprecated="auto",
    argon2__memory_cost = 65536,
    argon2__time_cost=2,
    argon2__parallelism=4
)

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain,hashed)->bool:
    return pwd_context.verify(plain,hashed)

def create_access_token(data:dict,expires_delta:timedelta|None=None)->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)+expires_delta
    else:
        expire = datetime.now(timezone.utc)+timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
