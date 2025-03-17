from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException
from auth_routers.auth import decode_jwt
from fastapi.templating import Jinja2Templates
from models import Book, User
from sqlalchemy.orm import Session
from lib_routers.utils import get_db
from fastapi.responses import HTMLResponse, RedirectResponse
import csv
from io import StringIO

templates = Jinja2Templates(directory='templates')

router = APIRouter(prefix='/library',
                   tags=['Library System'])

db_conn = Annotated[Session, Depends(get_db)]

@router.get('/book_page', response_class=HTMLResponse)
async def add_book_page(request: Request, db: db_conn):
    user_token = getattr(request.state, "user")
    user = db.query(User).filter(User.id == user_token['id']).first()
    return templates.TemplateResponse('add_book_page.html',
                                      context={'request': request, 'user': user})

@router.post('/book_page')
async def add_book_database(request: Request, db: db_conn,
                            book_name=Form(...), author=Form(...),
                            genre=Form(...), description: Optional[str] = Form(None),
                            language=Form(...), publisher: Optional[str] = Form(None),
                            publishing_year: Optional[int] = Form(None),
                            cover_image: UploadFile = File(None)):
    user = getattr(request.state, 'user')
    try:
        if cover_image is not None:
            cover_image = cover_image.file.read()
        else:
            cover_image = None

        if publishing_year is not None and publishing_year <= 0:
            return templates.TemplateResponse('add_book_page.html',
                                              context={'request': request,
                                                       'msg': 'Publishing year cannot be negative or zero.',
                                                       'user': user})

        book = Book(
            book_name=book_name,
            author=author,
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

        return RedirectResponse(url='/library/dashboard', status_code=302)
    except Exception as e:
        print(e)
        return templates.TemplateResponse('add_book_page.html',
                                          context={'request': request, 'msg': e, 'user': user})

# ✅ NEW BULK UPLOAD FEATURE
@router.post('/upload-books/')
async def upload_books(request: Request, file: UploadFile = File(...), db: db_conn):
    user = getattr(request.state, "user")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a valid CSV file.")

    content = await file.read()
    decoded_content = content.decode("utf-8")
    csv_reader = csv.reader(StringIO(decoded_content))

    # Skip the header row
    next(csv_reader, None)

    books_to_add = []

    for row in csv_reader:
        if len(row) < 6:  # Ensure row has enough columns
            continue

        book = Book(
            book_name=row[0],
            author=row[1],
            genre=row[2],
            language=row[3],
            description=row[4],
            publishing_year=int(row[5]) if row[5].isdigit() else None,
            available=True
        )
        books_to_add.append(book)

    db.add_all(books_to_add)
    db.commit()

    return {"message": f"{len(books_to_add)} books uploaded successfully!"}
