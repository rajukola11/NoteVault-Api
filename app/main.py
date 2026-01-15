from fastapi import FastAPI
from app.api.v1.note_routes import note_router

app = FastAPI()

app.include_router(note_router)
