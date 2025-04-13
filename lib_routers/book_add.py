from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request, Form
from auth_routers.auth import decode_jwt
from fastapi.templating import Jinja2Templates
from models import Book, User
from sqlalchemy.orm import Session
from lib_routers.utils import get_db
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import UploadFile, File

templates = Jinja2Templates(directory='templates')

router = APIRouter(prefix='/library',
                   tags=['Library System'])

db_conn = Annotated[Session,Depends(get_db)]

@router.get('/book_page',response_class=HTMLResponse)
async def add_book_page(request:Request, db:db_conn):
    user_token = getattr(request.state, "user")
    user = db.query(User).filter(User.id == user_token['id']).first()
    return templates.TemplateResponse('add_book_page.html',
                                      context={
                                          'request':request,'user':user
                                      })
    
@router.post('/book_page')
async def add_book_database(request:Request,db:db_conn,
                            book_name=Form(...),author=Form(...),
                            genre=Form(...),description:Optional[str]=Form(None),
                            language=Form(...),publisher:Optional[str]=Form(None),
                            publishing_year:Optional[int]=Form(None),
                            cover_image: UploadFile = File(None)):
    user = getattr(request.state,'user')
    try:
        if cover_image is not None:
            cover_image = cover_image.file.read()
        else:
            cover_image = None
            
        if publishing_year is not None and publishing_year <= 0 :
            return templates.TemplateResponse('add_book_page.html',
                                              context={
                                                  'request':request,
                                                  'msg':'Publishing year cannot be negative or zero.',
                                                  'user':user
                                              })
        
        book = Book(
            book_name=book_name,
            author = author,
            available=True,
            genre=genre,
            language=language,
            description=description,
            publisher=publisher,
            publishing_year=publishing_year,
            cover_image=cover_image
        )
        
        db.add(book)
        db.commit()
        db.refresh(book)
        
        return RedirectResponse(url='/library/dashboard',status_code=302)
    except Exception as e:
        print(e)
        return templates.TemplateResponse('add_book_page.html',
                                        context={
                                            'request':request,
                                            'msg':e,
                                            'user':user
                                        })
