from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class User(BaseModel):
    id: int
    email: EmailStr
    nickname: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    nickname: str = Field(..., min_length=1, max_length=10)
    password: str = Field(..., min_length=8, max_length=20)

    # Password 유효성 검사 (대문자, 소문자, 숫자, 특수문자 각각 최소 1개 포함 여부 검사)
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        # 대문자
        if not re.search(r'[A-Z]', v):
            raise ValueError("대문자를 최소 1개 포함해야 합니다.")
        # 소문자
        if not re.search(r'[a-z]', v):
            raise ValueError("소문자를 최소 1개 포함해야 합니다.")
        # 숫자
        if not re.search(r'[0-9]', v):
            raise ValueError("숫자를 최소 1개 포함해야 합니다.")
        # 특수문자
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("특수문자를 최소 1개 포함해야 합니다.")
        return v

class UserUpdate(BaseModel):
    nickname: str | None = Field(None, min_length=1, max_length=10)