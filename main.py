from fastapi import FastAPI
from database import engine
from models import Base
from auth_routers.auth import router as auth
from lib_routers.book_add import router as add_book_router
from lib_routers.dashboard import router as dashboard_router
from lib_routers.book_manage import router as manage_router
from fastapi.middleware.cors import CORSMiddleware
from middlewares_fastapi.TokenBucketMiddleware import TokenBucketRateLimiter
from middlewares_fastapi.JWTtokenExtraction import jwtTokenExtractor

app = FastAPI()

Base.metadata.create_all(engine)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["localhost:8000"],  # Allows all origins
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth)
app.include_router(add_book_router)
app.include_router(dashboard_router)
app.include_router(manage_router)

app.add_middleware(TokenBucketRateLimiter)
app.add_middleware(jwtTokenExtractor)