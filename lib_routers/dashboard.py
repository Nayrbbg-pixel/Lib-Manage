from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request, Form
from auth_routers.auth import decode_jwt
from fastapi.templating import Jinja2Templates
from models import Book
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
    user = decode_jwt(request)
    user_lib_books = db.query(Book).filter(Book.user_id==user['id']).all()
    if user is False:
        return RedirectResponse(url='/auth/login',status_code=302)
    if user['role'] == 'user':
         return RedirectResponse(url='/home',status_code=302)
    if q is not None:
        books=db.query(Book).filter(Book.user_id==user['id']).all()
        results = []
        for book in books:
            if q.lower() in book.book_name.lower() or q.lower() in book.author.lower() or q.lower() in book.genre.lower():
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