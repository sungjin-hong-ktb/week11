from fastapi import FastAPI

from app.database import Base, engine
from app.routers import user_router

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Community API",
    description="커뮤니티 백엔드 API",
    version="1.0.0"
)

app.include_router(user_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)