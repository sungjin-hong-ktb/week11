from sqlalchemy.orm import Session

from app.models.user_model import Users
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.utils.security import verify_password
from app.exceptions import UnauthorizedException


class AuthController:
    def __init__(self, db: Session):
        self.db = db

    def login(self, credentials: LoginRequest) -> LoginResponse:
        """로그인

        Args:
            credentials (LoginRequest): 로그인 정보 (이메일, 비밀번호)

        Returns:
            LoginResponse: 로그인 성공 메시지 및 사용자 정보

        Raises:
            ValueError: 이메일 또는 비밀번호가 잘못된 경우
        """
        # 이메일로 사용자 조회
        user = (
            self.db.query(Users)
            .filter(Users.email == credentials.email)
            .first()
        )

        if not user:
            raise UnauthorizedException("이메일 또는 비밀번호가 잘못되었습니다")

        # 비밀번호 검증
        if not verify_password(credentials.password, user.hashed_password):
            raise UnauthorizedException("이메일 또는 비밀번호가 잘못되었습니다")

        return LoginResponse(
            message="로그인 성공",
            user_id=user.id,
            email=user.email,
            nickname=user.nickname
        )
