from fastapi import FastAPI
from app.api.v1.note_routes import note_router
from app.api.v1.user_routes import user_router
from app.api.v1.auth_routes import auth_router

app = FastAPI()

app.include_router(note_router)
app.include_router(user_router)
app.include_router(auth_router)
