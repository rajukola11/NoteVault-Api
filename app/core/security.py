from passlib.context import CryptContext

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
