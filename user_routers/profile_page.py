from fastapi import APIRouter, HTTPException, Request, Depends, File, Response, UploadFile
from fastapi.responses import RedirectResponse, FileResponse
from user_routers.utils import get_db, templates
from typing import Annotated
from sqlalchemy.orm import Session
from models import User, ProfileImage

router = APIRouter()

db_conn = Annotated[Session, Depends(get_db)]

@router.get('/profile')
async def profile_page(request:Request, db:db_conn):
    user = getattr(request.state,'user')
    profile_image = db.query(ProfileImage).filter(ProfileImage.user_id==user['id']).first()
    if profile_image is None:
        profile_image = None
    user_data = db.query(User).filter(User.id==user['id']).first()
    return templates.TemplateResponse('profile-page.html',context={
        'request':request,'user':user_data,'image':profile_image
    })
    
@router.post('/profile')
async def profile_picture_upload(request:Request,db:db_conn,image:UploadFile=File(...)):
    user = getattr(request.state,'user')
    profile_image_check = db.query(ProfileImage).filter(ProfileImage.user_id==user['id']).first() 
    print(image.content_type)
    if not profile_image_check:
        profile_image = ProfileImage(user_id=user['id'],
                                    image_data=await image.read())
        db.add(profile_image)
        db.commit()
        db.refresh(profile_image)
    else:
        profile_image_check.image_data = await image.read()
        db.commit()
        db.refresh(profile_image_check)
    
    return RedirectResponse(url='/profile',status_code=302)

@router.get("/users/{user_id}/profile-image")
async def get_profile_image(user_id: int, db: Session = Depends(get_db)):
    profile_image = db.query(ProfileImage).filter(ProfileImage.user_id == user_id).first()

    if profile_image is None:
        return FileResponse('images/unknowuser.jpg', media_type="image/jpg")
    
    return Response(content=profile_image.image_data, media_type="image/jpeg")