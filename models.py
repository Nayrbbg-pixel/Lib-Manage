from datetime import datetime
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
    publisher = Column(String,nullable=True)
    publishing_year = Column(Integer,nullable=True)
    cover_image = Column(LargeBinary,nullable=True)
    
class ProfileImage(Base):
    __tablename__ = 'profile_image'
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('user.id'))
    image_data = Column(LargeBinary, nullable=True)
    
class BookComment(Base):
    __tablename__ = 'book_comment'
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('user.id'))
    book_id = Column(Integer,ForeignKey('book.id'))
    comment = Column(String,nullable=False)
    timestamp = Column(Date,nullable=False, default=datetime.now())
    
    
class Query(Base):
    __tablename__ = 'query'
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('user.id'))
    username = Column(String,nullable=False)
    # role = Column(Enum(Role),nullable=False)
    query = Column(String,nullable=False)
    timestamp = Column(Date,nullable=False, default=datetime.now())
    
class QueryResponse(Base):
    __tablename__ = 'query_response'
    
    id = Column(Integer,primary_key=True,index=True)
    query_id = Column(Integer,ForeignKey('query.id'))
    response = Column(String,nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    timestamp = Column(Date,nullable=False, default=datetime.now())