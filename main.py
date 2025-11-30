from fastapi import FastAPI

from app.database import Base, engine
from app.routers import user_router, post_router, comment_router, auth_router

app = FastAPI(
    title="Community API",
    description="커뮤니티 백엔드 API",
    version="1.0.0"
)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)