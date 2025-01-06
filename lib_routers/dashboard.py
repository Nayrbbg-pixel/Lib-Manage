from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request, Form
from auth_routers.auth import decode_jwt
from fastapi.templating import Jinja2Templates
from models import Book, User
from sqlalchemy.orm import Session
from lib_routers.utils import get_db
from fastapi.responses import HTMLResponse, RedirectResponse

db_conn = Annotated[Session,Depends(get_db)]
router = APIRouter(
    prefix='/library'
)

templates = Jinja2Templates(directory='templates')

@router.get('/dashboard',response_class=HTMLResponse)
async def dashboard_page(request:Request,db:db_conn,q:Optional[str]=None):
    user_token = getattr(request.state, "user")
    user = db.query(User).filter(User.id == user_token['id']).first()
    user_lib_books = db.query(Book).all()
    
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
        return templates.TemplateResponse('dashboard.html',context=
                                        {'request':request,
                                         'books':user_lib_books,
                                         'user':user})
    return templates.TemplateResponse('dashboard.html',context=
                                        {'request':request,
                                         'books':user_lib_books,
                                         'user':user})