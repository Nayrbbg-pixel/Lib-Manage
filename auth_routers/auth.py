from fastapi import APIRouter,Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from models import User, Role
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

templates = Jinja2Templates(directory='templates')

router = APIRouter(prefix='/auth')

SECRET_KEY = 'ddd57df0f6976aac2e3d44f426af6beac362dc6e15a411e1b60a8f054c537a13'
ALGORITHM = 'HS256'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_conn = Annotated[Session,Depends(get_db)]

@router.get('/register', response_class=HTMLResponse)
async def register_page(request:Request):
    return templates.TemplateResponse('register.html',context={
        'request':request
    })
    
def check_username_and_username(username:str,db:Session):
    username = db.query(User).filter(User.username==username).first()    
    if username is None:
        return True
    return False
    
@router.post('/register')
async def register_user_endpoint(request:Request,db:db_conn,username:str = Form(...),
                                 password1:str=Form(...),
                                 password2:str=Form(...)):
    
    if check_username_and_username(username=username,db=db):
        if password1==password2:
            
            password=bcrypt_context.hash(password1)
            user = User(
                username=username,
                password=password,
                role=Role.USER
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return templates.TemplateResponse('register.html',context={
                'request':request,'msg':'Successful Login!'
            })
        return templates.TemplateResponse('register.html',context={
                'request':request,'msg':'Passwords did not match!'
            })
    return templates.TemplateResponse('register.html',context={
                'request':request,'msg':'Username already exists!'
            })
    
    
def authenticate_user(username:str,password:str,db:Session):
    user = db.query(User).filter(User.username==username).first()
    if user is not None:
        if bcrypt_context.verify(password,user.password):
            return user
        return False
    return False

def create_jwt_token(role:str,id:int,username:str,expiry_delta:timedelta):
    encode = {
        'sub':username,
        'id':id,
        'role':role
    }
    exp = datetime.now() + expiry_delta
    encode['exp'] = exp
    token = jwt.encode(encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return token

class LoginForm:
    def __init__(self,request:Request):
        self.request:Request = request
        self.username:Optional[str] = None
        self.password:Optional[str] = None
    
    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.password = form.get('password')
        
@router.get('/login')
async def login_page(request:Request):
    return templates.TemplateResponse('login.html',context={
        'request':request
    })
    
async def store_access_token(response:Response,
                             db:Session=Depends(get_db),
                             form_data:OAuth2PasswordRequestForm=Depends(),
                            ):
    try:
        user=authenticate_user(form_data.username,form_data.password,db=db)
        if user is False:
            return False
        token = create_jwt_token(role=user.role.value,id=user.id,username=user.username,
                                    expiry_delta=timedelta(minutes=500))
        response.set_cookie(key='access_token',value=token,httponly=True,secure=True,
                            samesite='lax')
        return True
    except Exception as e:
        return False
    
@router.post('/login')
async def login_for_access_token(request:Request,
                                 db:Session=Depends(get_db)):
    try:
        form = LoginForm(request=request)
        await form.create_oauth_form()
        response = RedirectResponse(url='/library/dashboard',status_code=302)
        validation_cookie = await store_access_token(response=response,
                                                     form_data=form,db=db)
        if validation_cookie is False:
            return templates.TemplateResponse('login.html',context={
        'request':request,'msg':'Username or password is wrong!'
        })
        return response

    except Exception as e:
        return templates.TemplateResponse('login.html',context={
        'request':request,'msg':e
        })
        
def decode_jwt(request:Request):
    try:
        token:str =request.cookies.get('access_token')
        
        if token is None:
            return False
        
        payload:dict = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload['sub']
        id:int = payload['id']
        role:str = payload['role']
        
        if username is None or id is None:
            return False
        
        return {'username':username,'id':id,'role':role}
    except JWTError:
        return False

@router.get('/logout')
async def logout_user(request:Request):
    response = RedirectResponse(url='/auth/login',status_code=302)
    response.delete_cookie(key='access_token')
    return response