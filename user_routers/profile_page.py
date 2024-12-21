from fastapi import APIRouter, Request, Depends
from user_routers.utils import get_db, templates
from typing import Annotated
from sqlalchemy.orm import Session
from models import User

router = APIRouter()

db_conn = Annotated[Session, Depends(get_db)]

@router.get('/profile')
async def profile_page(request:Request, db:db_conn):
    user = getattr(request.state,'user')
    
    user_data = db.query(User).filter(User.username==user['username']).first()
    return templates.TemplateResponse('profile-page.html',context={
        'request':request,'user':user_data,'image':None
    })