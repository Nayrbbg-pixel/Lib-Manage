from fastapi import APIRouter, Depends, Form, Response, Request
from fastapi.responses import RedirectResponse
from comm_routers.utils import templates, get_db
from typing import Annotated
from sqlalchemy.orm import Session
from models import Query, QueryResponse, User

router = APIRouter()

db_conn = Annotated[Session, Depends(get_db)]

@router.get('/comms-query-reply/{query_id}')
async def reply_page(request:Request, db:db_conn, query_id:int):
    query_details = db.query(Query).filter(Query.id == query_id).first()
    user_token = getattr(request.state,'user')
    user = db.query(User).filter(User.id == user_token['id']).first()
    if query_details is None:
        return RedirectResponse(url='/home',status_code=302)
    
    responses = db.query(QueryResponse).filter(QueryResponse.query_id == query_id).all()[::-1]
    
    response_users = []
    for response in responses:
        user= db.query(User).filter(User.id == response.user_id).first()
        response_users.append(user)
        
    return templates.TemplateResponse('query_responses-page.html',
                                      context={'request':request,
                                               'responses':responses,
                                               'query':query_details,
                                               'user':user,
                                               'response_users':response_users})
    
@router.post('/comms-query-reply/{query_id}')
async def save_reply(request:Request, db:db_conn,query_id:int,
                     response:str=Form(str)):
    
    if response is None:
        return RedirectResponse(url=f'/comms-query-reply/{query_id}',status_code=302)
    
    user_token = getattr(request.state,'user')
    user = db.query(User).filter(User.id==user_token['id']).first()
    
    query_response = QueryResponse(
        response=response,
        user_id = user.id,
        query_id = query_id
    )
    
    db.add(query_response)
    db.commit()
    db.refresh(query_response)
    
    return RedirectResponse(url=f'/comms-query-reply/{query_id}',status_code=302)