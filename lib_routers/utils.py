from database import SessionLocal
from fastapi.templating import Jinja2Templates

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
