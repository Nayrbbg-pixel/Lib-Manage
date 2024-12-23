from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request, Form, Response
from auth_routers.auth import decode_jwt
from fastapi.templating import Jinja2Templates
from models import Book
from sqlalchemy.orm import Session
from lib_routers.utils import get_db
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi import UploadFile, File

router = APIRouter(prefix='/library')

db_conn = Annotated[Session,Depends(get_db)]
templates = Jinja2Templates(directory='templates')

@router.get('/manage-book/{title}/{book_id}')
async def manage_book_page(title:str,book_id:int,
                           db:db_conn,request:Request):
    
    book = db.query(Book).filter(Book.id==book_id,Book.book_name==title).\
        first()
        
    if book is None:
        return RedirectResponse(url='/library/dashboard',status_code=302)
    
    return templates.TemplateResponse('manage-book.html',context={
        'request':request,'book':book,'user': getattr(request.state,'user')
    })
    
@router.post('/manage-book/{title}/{book_id}')
async def manage_book_post_api(request:Request,db:db_conn,title:str,book_id:int,
                               book_name:str=Form(...),author:str=Form(...),genre:str=Form(...),
                               availability:str=Form(...),return_date:Optional[str]=Form(None),
                               language:str=Form(...),description:str=Form(...),publisher:Optional[str]=Form(None),
                               publishing_year:Optional[int]=Form(None),cover_image:UploadFile=File(None)):
        
    book=db.query(Book).filter(Book.id==book_id).first()

    parsed_date = datetime.strptime(return_date, "%Y-%m-%d").date() if return_date else None
    
    if parsed_date and parsed_date < datetime.today().date():
        return templates.TemplateResponse('manage-book.html',context={
        'request':request,'book':book,'msg':'Return date cannot be in the past.'
    })
    
    book.book_name = book_name
    book.author = author
    
    if availability == 'Yes':
        availability = True
    else:
        availability = False
        
    if availability is True:
        parsed_date = None
        
    if not availability:
        if parsed_date is None:
            return templates.TemplateResponse('manage-book.html',context={
        'request':request,'book':book,'msg':'Return date is not given.'})
            
    if publishing_year is not None and publishing_year <= 0:
        return templates.TemplateResponse('manage-book.html',context={
        'request':request,'book':book,'msg':'Invalid publishing year.'})
     

    try:
        print(cover_image.file.read()[0])
        book.cover_image = cover_image.file.read()
    except:
        book.cover_image = book.cover_image
                
    # print(image_data[0])
                
    book.available = availability
    book.return_date = parsed_date
    book.genre = genre
    book.description = description
    book.language = language
    book.publisher = publisher
    book.publishing_year = publishing_year
    
    db.commit()
    db.refresh(book)
    
    return RedirectResponse(url='/library/dashboard',status_code=302)

@router.get('/delete/{book_id}')
async def delete_book_element(request:Request,db:db_conn,book_id:int):
    book = db.query(Book).filter(Book.id==book_id).first()
    
    if book is None:
        return RedirectResponse(url='/library/dashboard',status_code=302)
    
    db.delete(book)
    db.commit()
    
    return RedirectResponse(url='/library/dashboard',status_code=302)
