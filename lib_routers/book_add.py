from typing import Annotated
from fastapi import APIRouter, Depends, Request, Form
from auth_routers.auth import decode_jwt
from fastapi.templating import Jinja2Templates
from models import Book
from sqlalchemy.orm import Session
from lib_routers.utils import get_db
from fastapi.responses import HTMLResponse, RedirectResponse

templates = Jinja2Templates(directory='templates')

router = APIRouter(prefix='/library',
                   tags=['Library System'])

db_conn = Annotated[Session,Depends(get_db)]

@router.get('/book_page',response_class=HTMLResponse)
async def add_book_page(request:Request):
    user = decode_jwt(request)
    if user is False:
        return RedirectResponse(url='/auth/login',status_code=302)
    return templates.TemplateResponse('add_book_page.html',
                                      context={
                                          'request':request
                                      })
    
@router.post('/book_page')
async def add_book_database(request:Request,db:db_conn,
                            book_name=Form(...),author=Form(...)):
    try:
        book = Book(
            book_name=book_name,
            author = author,
            available=True
        )
        
        db.add(book)
        db.commit()
        db.refresh(book)
        
        return templates.TemplateResponse('add_book_page.html',
                                        context={
                                            'request':request,
                                            'msg':'Successfully added the book!'
                                        })
    except:
        return templates.TemplateResponse('add_book_page.html',
                                        context={
                                            'request':request,
                                            'msg':'Failed to add the book!'
                                        })