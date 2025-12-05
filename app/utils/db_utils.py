from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import InvalidDataException, DatabaseException


@contextmanager
def db_transaction(db: Session):
    """데이터베이스 트랜잭션 컨텍스트 매니저
    Usage:
        with db_transaction(self.db):
            self.db.add(new_object)
        
    Args:
        db (Session): SQLAlchemy 세션

    Raises:
        InvalidDataException: IntegrityError 발생 시
        DatabaseException: 기타 SQLAlchemy 에러 발생 시
    """
    try:
        yield db
        db.commit()
    except IntegrityError:
        db.rollback()
        raise InvalidDataException("유효하지 않은 데이터입니다")
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseException(f"데이터베이스 오류가 발생했습니다: {str(e)}")
