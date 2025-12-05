from fastapi import status


class AppException(Exception):
    """기본 앱 예외"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# 리소스 관련
class NotFoundException(AppException):
    """리소스를 찾을 수 없을 때"""
    def __init__(self, message: str = "리소스를 찾을 수 없습니다"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class AlreadyExistsException(AppException):
    """리소스가 이미 존재할 때"""
    def __init__(self, message: str = "이미 존재하는 리소스입니다"):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


# 권한 관련
class UnauthorizedException(AppException):
    """인증되지 않은 사용자"""
    def __init__(self, message: str = "인증이 필요합니다"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    """권한이 없을 때"""
    def __init__(self, message: str = "권한이 없습니다"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


# 데이터 검증 관련
class InvalidDataException(AppException):
    """유효하지 않은 데이터"""
    def __init__(self, message: str = "유효하지 않은 데이터입니다"):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


# 데이터베이스 관련
class DatabaseException(AppException):
    """데이터베이스 오류"""
    def __init__(self, message: str = "데이터베이스 오류가 발생했습니다"):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
