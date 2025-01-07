from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse, JSONResponse
from comm_routers.utils import templates, get_db
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from models import Query, User

router = APIRouter()

db_conn = Annotated[Session, Depends(get_db)]

@router.get('/comms-query-page')
async def comms_query_page(request: Request, db: db_conn):
    queries = db.query(Query).all()[::-1]
    user_token = getattr(request.state,'user')
    user = db.query(User).filter(User.id==user_token['id']).first()
    return templates.TemplateResponse("comms_query_page.html", 
                                      {"request": request,
                                       "queries":queries,
                                       "user":user})
    
@router.post('/comms-query-page')
async def post_query(request: Request, db: db_conn,
                        query: str = Form(None)):
        user_token = getattr(request.state,'user')
        user = db.query(User).filter(User.id==user_token['id']).first()
        
        if query is None:
            return JSONResponse(content={"success": False,
                                        "error": "Query is required"},
                                status_code=400)
        
        query = Query(
            user_id = user.id,
            username = user.username,
            query = query
        )
        
        db.add(query)
        db.commit()
        db.refresh(query)
        
        return RedirectResponse(url='/comms-query-page',status_code=302)
    
