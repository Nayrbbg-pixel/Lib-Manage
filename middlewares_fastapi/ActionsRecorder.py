from starlette.middleware.base import BaseHTTPMiddleware
from database import SessionLocal
from models import User, UserRecordDetails

class ActionRecorderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app=app)
        
    async def dispatch(self, request, call_next):
        
        print('AR')
        
        if request.url.path.startswith('/auth'):
            return await call_next(request)
        
        db = SessionLocal()
        user_token = getattr(request.state, 'user')
        user = db.query(User).filter(User.id==user_token['id']).first()
        
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
            
        if '/home' in path:
            action = f'Path: {path}\nMethod: {method}\nObjective: Viewing the library.'
            
        if '/books' in path:
            action = f'Path {path}\nMethod: {method}\nObjective: Viewing a book in the library details page.'
           
        if 'profile' not in path:
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
        return await call_next(request)