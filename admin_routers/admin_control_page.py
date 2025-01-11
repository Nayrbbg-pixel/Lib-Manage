from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from admin_routers.utils import get_db, templates
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from models import User, UserRecordDetails, Role
from auth_routers.auth import check_username_and_username

router = APIRouter()

db_conn = Annotated[Session,Depends(get_db)]

@router.get('/admin/user-details/{user_id}')
async def user_control_page(request:Request, db:db_conn,
                            user_id:int):
    user_token = getattr(request.state,'user')
    user = db.query(User).filter(User.id == user_token['id']).first()
    req_user = db.query(User).filter(User.id == user_id).first()
    user_records = db.query(UserRecordDetails).filter(UserRecordDetails.user_id==req_user.id).all()[::-1]
    
    if req_user.role.value == 'admin':
        return RedirectResponse(url='/admin/home',
                                status_code=302)
    
    if req_user is None:
        return RedirectResponse(url='/admin/home',
                                status_code=302)
    
    
    return templates.TemplateResponse('admin_control_page.html',
                                      context={'request':request,
                                               'user_records':user_records,
                                               'user':user,
                                               'target_user':req_user})
    
@router.post('/admin/user-details/{user_id}')
async def user_control_page(request:Request, db:db_conn,
                            user_id:int, username:str=Form(...),
                            role=Form(...)):
    
    user_token = getattr(request.state,'user')
    user = db.query(User).filter(User.id == user_token['id']).first()
    req_user = db.query(User).filter(User.id == user_id).first()
    user_records = db.query(UserRecordDetails).filter(UserRecordDetails.user_id==req_user.id).all()[::-1]    
    
    if req_user.role.value == 'admin':
        return RedirectResponse(url='/admin/home',
                                status_code=302)
    
    if req_user is None:
        return RedirectResponse(url='/admin/home',
                                status_code=302)
      
    username_check = db.query(User).filter(User.username == username).first()
      
    if username_check is not None and username_check.id != req_user.id:  
        return templates.TemplateResponse('admin_control_page.html',
                                    context={'request':request,
                                            'user_records':user_records,
                                            'user':user,
                                            'target_user':req_user,
                                            'error_message':'Username is already taken!'})
    if role == 'Admin':
        role = Role.ADMIN
    elif role == 'Inspector':
        role = Role.INSPECTOR
    elif role == 'User':
        role = Role.USER
    
    req_user.username = username
    req_user.role = role
    
    db.commit()
    db.refresh(req_user)
    
    return RedirectResponse(url=f'/admin/user-details/{user_id}',
                            status_code=302)
    
@router.get('/admin/delete-user/{user_id}')
async def user_delete(request:Request, db:db_conn,
                            user_id:int):
    user_token = getattr(request.state,'user')
    user = db.query(User).filter(User.id == user_token['id']).first()
    req_user = db.query(User).filter(User.id == user_id).first()
    
    if req_user.role.value == 'admin':
        return RedirectResponse(url='/admin/home',
                                status_code=302)
    
    if req_user is None:
        return RedirectResponse(url='/admin/home',
                                status_code=302)
    
    user_records = db.query(UserRecordDetails).filter(UserRecordDetails.user_id == req_user.id).all()
    
    for user_record in user_records:
        db.delete(user_record)
        db.commit()    
    
    db.delete(req_user)
    db.commit()
    
    return RedirectResponse(url='/admin/home',
                                status_code=302)