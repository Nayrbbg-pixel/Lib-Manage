from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from auth_routers.auth import decode_jwt

class jwtTokenExtractor(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app)
    
    async def dispatch(self, request, call_next):
        
        print(request.url.path)
        
        if request.url.path.startswith('/auth'):
            return await call_next(request)
        
        jwt_token = decode_jwt(request)
        
        if request.url.path.startswith('/admin') and jwt_token['role']!='admin':
            return RedirectResponse(url='/home',status_code=302)
        
        if not jwt_token and request.url.path != '/':
            return RedirectResponse(url='/auth/login',status_code=302)
        
        request.state.user = jwt_token

        if request.url.path.startswith('/library') and jwt_token['role'] =='user' :
            return RedirectResponse(url='/home',status_code=302)
        return await call_next(request)
