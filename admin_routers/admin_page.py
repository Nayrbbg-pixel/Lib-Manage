from fastapi import APIRouter, Depends, Request
from admin_routers.utils import get_db, templates
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from models import User

router = APIRouter()

db_conn = Annotated[Session,Depends(get_db)]

@router.get('/admin/home')
async def admin_home_page(request:Request, db:db_conn,
                          q:Optional[str]=None):
    user_token = getattr(request.state,'user')
    user = db.query(User).filter(User.id == user_token['id']).first()
    users = db.query(User).all()
    
    if q is not None:
        user_list = []
        for user in users:
            if q.lower() in user.username.lower() or q.lower() in user.role.value.lower():
                user_list.append(user)
            else:
                continue
        users = user_list
    
    return templates.TemplateResponse('admin_home_page.html',
                                      context={'request':request,
                                               'users':users,
                                               'user':user})