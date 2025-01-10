from fastapi.templating import Jinja2Templates
from database import SessionLocal

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
