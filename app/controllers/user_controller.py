from sqlalchemy.orm import Session

from app.models.user_model import Users
from app.schemas.user_schema import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> Users:
    """회원 생성

    Args:
        db (Session): 데이터베이스 세션
        user_data (UserCreate): 생성할 회원 정보

    Returns:
        Users: 생성된 회원 정보

    Raises:
        ValueError: 이메일이 이미 사용 중인 경우
    """
    existing_email = db.query(Users).filter(Users.email == user_data.email).first()
    if existing_email:
        raise ValueError("이미 사용중인 이메일입니다.")

    new_user = Users(
        email=user_data.email,
        nickname=user_data.nickname,
        password=user_data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def get_users(db: Session) -> list[Users]:
    """모든 회원정보 조회

    Args:
        db (Session): 데이터베이스 세션

    Returns:
        list[Users]: 모든 회원 정보 리스트
    """
    return db.query(Users).all()


def get_user_by_id(db: Session, user_id: int) -> Users | None:
    """id로 회원정보 조회

    Args:
        db (Session): 데이터베이스 세션
        user_id (int): 회원 id

    Returns:
        Users | None: 회원 정보 또는 None
    """
    return db.query(Users).filter(Users.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Users | None:
    """회원정보 수정 (닉네임만 수정 가능)

    Args:
        db (Session): 데이터베이스 세션
        user_id (int): 회원 id
        user_data (UserUpdate): 수정할 회원 정보

    Returns:
        Users | None: 수정된 회원 정보 또는 None

    Raises:
        ValueError: 닉네임이 이미 사용 중인 경우
    """
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        return None

    # nickname이 제공된 경우에만 중복 체크 및 업데이트
    if user_data.nickname:
        existing_nickname = db.query(Users).filter(
            Users.nickname == user_data.nickname,
            Users.id != user_id
        ).first()

        if existing_nickname:
            raise ValueError("이미 사용중인 닉네임입니다.")

        user.nickname = user_data.nickname

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> Users | None:
    """회원정보 삭제

    Args:
        db (Session): 데이터베이스 세션
        user_id (int): 회원 id

    Returns:
        Users | None: 삭제된 회원 정보 또는 None
    """
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
