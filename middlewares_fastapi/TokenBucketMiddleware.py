from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from TokenBucketAlgorithm import TokenBucket
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from starlette import status
from user_routers.utils import templates

class TokenBucketRateLimiter(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app=app)
        self.tokenBucket = TokenBucket(100,2)
        
    async def dispatch(self,request:Request,call_next):
        rate_limit_check = self.tokenBucket.allow_request()
        if rate_limit_check:
            return await call_next(request)

        return templates.TemplateResponse('rate-limit.html',context={
            'request':request
        })