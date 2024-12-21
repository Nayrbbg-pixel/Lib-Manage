from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from TokenBucketAlgorithm import TokenBucket
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from starlette import status

class TokenBucketRateLimiter(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app=app)
        self.tokenBucket = TokenBucket(10,2)
        
    async def dispatch(self,request:Request,call_next):
        rate_limit_check = self.tokenBucket.allow_request()
        if rate_limit_check:
            return await call_next(request)
        block_period = datetime.now() + timedelta(seconds=5)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={
                'msg':f'Your rate limit has been reached. Please try again after {block_period} seconds.'
            }
        )