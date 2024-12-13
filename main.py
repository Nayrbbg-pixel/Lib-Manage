from fastapi import FastAPI
from database import engine
from models import Base, User, Role
from auth_routers.auth import router as auth
from lib_routers.book_add import router as add_book_router

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(auth)
app.include_router(add_book_router)