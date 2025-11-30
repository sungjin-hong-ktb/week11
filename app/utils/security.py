from passlib.context import CryptContext

# bcrypt 해싱 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """비밀번호 해싱

    Args:
        password (str): 평문 비밀번호

    Returns:
        str: 해싱된 비밀번호
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증

    Args:
        plain_password (str): 평문 비밀번호
        hashed_password (str): 해싱된 비밀번호

    Returns:
        bool: 비밀번호 일치 여부
    """
    return pwd_context.verify(plain_password, hashed_password)
