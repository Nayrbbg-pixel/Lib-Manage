from fastapi import APIRouter, Request, Depends
from user_routers.utils import templates, get_db
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from models import ProfileImage, Book, User

db_conn = Annotated[Session, Depends(get_db)]

router = APIRouter()

@router.get('/home')
async def home_page(request:Request, db:db_conn, q:Optional[str]=None):
    user_token = getattr(request.state,'user')
    user_lib_books = db.query(Book).all()
    
    user = db.query(User).filter(User.id==user_token['id']).first()
    
    if q is not None:
        books=db.query(Book).all()
        results = []
        for book in books:
            
            if not book.publisher:
                book.publisher = '52fe088583e4a8bf3dee'
            if book.publishing_year is None:
                book.publishing_year = '52fe088583e4a8bf3dee'
            
            if q.isdigit():
                if q == str(book.publishing_year):
                    results.append(book)
                    continue
            elif q.lower() in book.book_name.lower() or q.lower() in book.author.lower() or q.lower() in book.genre.lower() or q.lower() in book.publisher.lower() or q.lower() in book.language.lower():
                results.append(book)
            else:
                continue
        user_lib_books = results
        return templates.TemplateResponse('home-page.html',context=
                                        {'request':request,
                                         'books':user_lib_books,
                                         'user':user})
    
    return templates.TemplateResponse('home-page.html',context={
        'request':request,'user':user,'books':user_lib_books
    })