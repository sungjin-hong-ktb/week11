from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    message: str = Field(description="응답 메시지")
    user_id: int = Field(description="사용자 ID")
    email: str = Field(description="이메일 주소")
    nickname: str = Field(description="닉네임")
