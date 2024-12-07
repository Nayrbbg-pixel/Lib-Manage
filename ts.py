from database import SessionLocal
from models import User


user = SessionLocal().query(User).filter(User.username=='Aryan Raj').first()
print(
    f"{user.username} | {user.role.value} | {user.password}"
)