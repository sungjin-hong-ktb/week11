from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.routers import user_router, post_router, comment_router, auth_router
from app.exceptions import AppException

app = FastAPI(
    title="Community API",
    description="커뮤니티 백엔드 API",
    version="1.0.0"
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": request.url.path
        }
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "error": "DatabaseError",
            "message": "데이터베이스 오류가 발생했습니다",
            "path": request.url.path
        }
    )

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)