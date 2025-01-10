from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from auth_routers.auth import decode_jwt
from models import User, UserRecordDetails
from database import SessionLocal

class jwtTokenExtractor(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app)
    
    async def dispatch(self, request, call_next):
        
        print(request.url.path)
        
        if request.url.path.startswith('/auth'):
            return await call_next(request)
        
        jwt_token = decode_jwt(request)
        request.state.user = jwt_token
        
        db = SessionLocal()
        
        user = db.query(User).filter(User.id==jwt_token['id']).first()
        
        path = request.url.path
        method = request.method
        action = 'No special action recorded for privacy.'
        
        if 'book_page' in path and method=='GET':
            action = f'Path: {path}\nMethod: {method}\nObjective: To add book.'
        
        if 'manage-book' in path and method == 'GET':
            action = f'Path: {path}\nMethod: {method}\nObjective: Editing Book.'
            
        if 'dashboard' in path:
            action = f'Path: {path}\nMethod: {method}\nObjective: Managing the dashboard.'
            
        if '/library/delete' in path:
            action = f'Path: {path}\nMethod: {method}\nObjective: Deleting a saved book.'
            
        if '/home' == path:
            action = f'Path: {path}\nMethod: {method}\nObjective: Viewing the library.'
            
        if '/books' in path:
            action = f'Path {path}\nMethod: {method}\nObjective: Viewing a book in the library details page.'
           
        if 'profile' not in path or 'cover-image' not in path:
            record = UserRecordDetails(
                username = user.username,
                role = user.role,
                user_id = user.id,
                path = path,
                method = method,
                action = action,
            )
        
            db.add(record)
            db.commit()
            db.refresh(record)
        
        if request.url.path.startswith('/admin') and jwt_token['role']!='admin':
            return RedirectResponse(url='/home',status_code=302)
        
        if not jwt_token and request.url.path != '/':
            return RedirectResponse(url='/auth/login',status_code=302)
        

        if request.url.path.startswith('/library') and jwt_token['role'] =='user' :
            return RedirectResponse(url='/home',status_code=302)
        
        
        return await call_next(request)