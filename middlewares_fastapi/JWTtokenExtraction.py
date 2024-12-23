from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from auth_routers.auth import decode_jwt

class jwtTokenExtractor(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app)
    
    async def dispatch(self, request, call_next):
        
        if request.url.path.startswith('/auth'):
            return await call_next(request)
        
        jwt_token = decode_jwt(request)
        
        if not jwt_token:
            return RedirectResponse(url='/auth/login',status_code=302)
        
        request.state.user = jwt_token

        if request.url.path.startswith('/library') and jwt_token['role'] =='user' :
            return RedirectResponse(url='/home',status_code=302)
        return await call_next(request)
