from fastapi import FastAPI
from database import engine
from models import Base, User, Role
from routers.auth import router as auth

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(auth)