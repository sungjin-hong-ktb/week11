from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import LoginResponse
from app.controllers.auth_controller import AuthController
from app.exceptions import UnauthorizedException

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    "/login",
    response_model=LoginResponse,
    description="OAuth2 표준 폼을 사용한 로그인"
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """로그인 (OAuth2 표준)

    Args:
        form_data (OAuth2PasswordRequestForm): OAuth2 폼 데이터 (username, password)
        db (Session): 데이터베이스 세션

    Returns:
        LoginResponse: 로그인 성공 메시지 및 사용자 정보

    Raises:
        HTTPException: 이메일 또는 비밀번호가 잘못된 경우
    """
    try:
        controller = AuthController(db)
        return controller.login(form_data.username, form_data.password)
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="로그아웃"
)
def logout():
    """로그아웃

    Returns:
        dict: 로그아웃 성공 메시지
    """
    return {"message": "로그아웃 성공"}
