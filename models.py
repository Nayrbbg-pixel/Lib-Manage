from database import Base
from sqlalchemy import Column, Integer, String,Enum 
from enum import Enum as pyEnum

class Role(str,pyEnum):
    ADMIN = 'admin'
    INSPECTOR = 'inspector'
    USER = 'user'

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String(50), unique=True,nullable=False)
    password = Column(String,nullable=False)
    role = Column(Enum(Role),nullable=False)