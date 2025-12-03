from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.user_model import Users
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.security import hash_password


class UserController:
    """사용자 관련 비즈니스 로직을 처리하는 컨트롤러"""

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
            raise ValueError("이미 사용중인 이메일입니다.")

        new_user = Users(
            email=user_data.email,
            nickname=user_data.nickname,
            hashed_password=hash_password(user_data.password)
        )
        
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("유효하지 않은 데이터입니다")
        except SQLAlchemyError:
            self.db.rollback()
            raise RuntimeError("데이터베이스 오류가 발생했습니다")

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

        # nickname이 제공된 경우에만 중복 체크 및 업데이트
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
                raise ValueError("이미 사용중인 닉네임입니다.")

            user.nickname = user_data.nickname

        try:
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("유효하지 않은 데이터입니다")
        except SQLAlchemyError:
            self.db.rollback()
            raise RuntimeError("데이터베이스 오류가 발생했습니다")
        
        return user

    def delete_user(self, user_id: int) -> Users | None:
        """회원정보 삭제

        Args:
            user_id (int): 회원 id

        Returns:
            Users | None: 삭제된 회원 정보 또는 None
        """
        user = (
            self.db.query(Users)
            .filter(Users.id == user_id)
            .first()
        )
        if user:
            try:
                self.db.delete(user)
                self.db.commit()
            except SQLAlchemyError:
                self.db.rollback()
                raise RuntimeError("데이터베이스 오류가 발생했습니다")
            
        return user
