from fastapi import APIRouter, Form, Request, Depends
from comm_routers.utils import get_db, templates
from typing import Annotated
from sqlalchemy.orm import Session
from models import User, Role

router = APIRouter()
db_conn = Annotated[Session, Depends(get_db)]

@router.get('/admin/update-role')
async def update_role_page(request:Request,db:db_conn):
    return templates.TemplateResponse('dev_role_manage.html',
                                      context={
                                          'request':request
                                      })
    
@router.post('/admin/update-role')
async def update_user_role(request:Request,db:db_conn,
                           username:str=Form(...)):
    user = db.query(User).filter(User.username==username).first()
    print(username)
    if user is None:
        return templates.TemplateResponse('dev_role_manage.html',
                                      context={
                                          'request':request,
                                          'msg':'User does not exist!'
                                      })
        
    user.role = Role.ADMIN
    
    db.commit()
    db.refresh(user)
    
    return templates.TemplateResponse('dev_role_manage.html',
                                      context={
                                          'request':request,
                                          'msg':'Done!!'
                                      })