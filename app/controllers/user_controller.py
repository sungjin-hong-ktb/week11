from sqlalchemy.orm import Session

from app.models.user_model import Users
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.security import hash_password
from app.exceptions import AlreadyExistsException
from app.utils.db_utils import db_transaction


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> Users:
        """회원 생성

        Args:
            user_data (UserCreate): 생성할 회원 정보

        Returns:
            Users: 생성된 회원 정보

        Raises:
            ValueError: 이메일이 이미 사용 중인 경우
        """
        existing_email = (
            self.db.query(Users)
            .filter(Users.email == user_data.email)
            .first()
        )
        if existing_email:
            raise AlreadyExistsException("이미 사용중인 이메일입니다.")

        new_user = Users(
            email=user_data.email,
            nickname=user_data.nickname,
            hashed_password=hash_password(user_data.password)
        )

        with db_transaction(self.db):
            self.db.add(new_user)

        self.db.refresh(new_user)
        return new_user

    def get_users(self) -> list[Users]:
        """모든 회원정보 조회

        Returns:
            list[Users]: 모든 회원 정보 리스트
        """
        return self.db.query(Users).all()

    def get_user_by_id(self, user_id: int) -> Users | None:
        """id로 회원정보 조회

        Args:
            user_id (int): 회원 id

        Returns:
            Users | None: 회원 정보 또는 None
        """
        return (
            self.db.query(Users)
            .filter(Users.id == user_id)
            .first()
        )

    def update_user(
        self,
        user_id: int,
        user_data: UserUpdate
    ) -> Users | None:
        """회원정보 수정 (닉네임만 수정 가능)

        Args:
            user_id (int): 회원 id
            user_data (UserUpdate): 수정할 회원 정보

        Returns:
            Users | None: 수정된 회원 정보 또는 None

        Raises:
            ValueError: 닉네임이 이미 사용 중인 경우
        """
        user = self.get_user_by_id(user_id)
        
        if not user:
            return None

        # 닉네임 중복 체크
        if user_data.nickname:
            existing_nickname = (
                self.db.query(Users)
                .filter(
                    Users.nickname == user_data.nickname,
                    Users.id != user_id
                )
                .first()
            )

            if existing_nickname:
                raise AlreadyExistsException("이미 사용중인 닉네임입니다.")

            user.nickname = user_data.nickname

        with db_transaction(self.db):
            pass  # commit만 수행

        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> Users | None:
        """회원정보 삭제

        Args:
            user_id (int): 회원 id

        Returns:
            Users | None: 삭제된 회원 정보 또는 None
        """
        user = self.get_user_by_id(user_id)
        
        if user:
            with db_transaction(self.db):
                self.db.delete(user)

        return user
