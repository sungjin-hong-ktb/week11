from fastapi import FastAPI

from app.database import Base, engine
from app.routers import user_router

app = FastAPI(
    title="Community API",
    description="커뮤니티 백엔드 API",
    version="1.0.0"
)

app.include_router(user_router.router)