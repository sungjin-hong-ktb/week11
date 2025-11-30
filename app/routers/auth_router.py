from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.controllers.auth_controller import AuthController

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """로그인

    Args:
        credentials (LoginRequest): 로그인 정보 (이메일, 비밀번호)
        db (Session): 데이터베이스 세션

    Returns:
        LoginResponse: 로그인 성공 메시지 및 사용자 정보

    Raises:
        HTTPException: 이메일 또는 비밀번호가 잘못된 경우
    """
    try:
        controller = AuthController(db)
        return controller.login(credentials)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    """로그아웃

    Returns:
        dict: 로그아웃 성공 메시지
    """
    return {"message": "로그아웃 성공"}
