from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from user_routers.utils import templates, get_db
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from models import Book, BookComment, User

router = APIRouter()

db_conn = Annotated[Session, Depends(get_db)]

@router.get("/books/{book_id}")
async def book_details(request:Request,book_id: int, 
                       db: db_conn):
    user = getattr(request.state, "user")
    book = db.query(Book).filter(Book.id == book_id).first()
    comments = db.query(BookComment).filter(BookComment.book_id == book_id).all()[::-1]
    username_list = []
    
    for comment in comments:
        username=db.query(User).filter(User.id==comment.user_id).first()
        username_list.append(username.username)
    
    return templates.TemplateResponse("book_details.html", {"request": request,
                                                            "user": user,
                                                            "book": book,
                                                            "comments": comments,
                                                            "username_list": username_list
                                                            })
    
@router.post("/books/{book_id}")
async def post_comments(request:Request,book_id:int,db:db_conn,
                        comment:str=Form(None),
                        ):
    user = getattr(request.state,'user')
    book = db.query(Book).filter(Book.id==book_id).first()
    
    if book is None:
        return RedirectResponse(url='/home',status_code=302)
    
    if comment is None:
        return RedirectResponse(url=f'/books/{book_id}',status_code=302)
    
    book_comment = BookComment(
        user_id = user['id'],
        book_id = book_id,
        comment = comment
    )
    
    db.add(book_comment)
    db.commit()
    db.refresh(book_comment)
    
    return RedirectResponse(url=f'/books/{book_id}',status_code=302)

@router.post("/books/{book_id}/{comment_id}/edit-comment")
async def edit_comment(request: Request, book_id: int, comment_id: int, db: db_conn,
                       edited_comment: Annotated[str, Form(...)]):
    user = getattr(request.state, 'user')
    print(edited_comment)
    book = db.query(Book).filter(Book.id == book_id).first()
    comment = db.query(BookComment).filter(BookComment.id == comment_id).first()

    if user['id'] != comment.user_id:
        return JSONResponse(content={"success": False, "error": "Unauthorized"}, status_code=403)

    if book is None or comment is None:
        return JSONResponse(content={"success": False, "error": "Not found"}, status_code=404)

    comment.comment = edited_comment

    db.commit()
    db.refresh(comment)

    return JSONResponse(content={"success": True})

@router.post("/books/{book_id}/{comment_id}/delete-comment")
async def delete_comment(request: Request, book_id: int, comment_id: int, db: db_conn):
    user = getattr(request.state, 'user')
    book = db.query(Book).filter(Book.id == book_id).first()
    comment = db.query(BookComment).filter(BookComment.id == comment_id).first()

    if user['id'] != comment.user_id:
        return JSONResponse(content={"success": False, "error": "Unauthorized"}, status_code=403)

    if book is None or comment is None:
        return JSONResponse(content={"success": False, "error": "Not found"}, status_code=404)

    db.delete(comment)
    db.commit()

    return JSONResponse(content={"success": True})

@router.get('/cover-image/{book_id}')
async def get_cover_image(book_id:int,db:db_conn):
    
    book = db.query(Book).filter(Book.id==book_id).first()
    
    headers={"Cache-Control":"no-store, no-cache, must-revalidate, max-age=0"}
    val = None
    # print(book.cover_image)
    try:
        book.cover_image[0]
        val = True
    except:
        val = False

    if val is False:
        return FileResponse('images/book_cover.jpeg',media_type='image/jpeg', headers=headers)
    
    return Response(content=book.cover_image,headers=headers)