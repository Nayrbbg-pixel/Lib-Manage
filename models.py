from database import Base
from sqlalchemy import (Column, Integer, String,
                        Enum, Boolean, Date,
                        ForeignKey, LargeBinary)
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
    
class Book(Base):
    __tablename__ = 'book'
    
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String,nullable=False)
    author = Column(String,nullable=False)
    available = Column(Boolean,nullable=False)
    return_date = Column(Date,nullable=True)
    genre = Column(String)
    description = Column(String)
    language = Column(String)
    
class ProfileImage(Base):
    __tablename__ = 'profile_image'
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('user.id'))
    image_data = Column(LargeBinary)