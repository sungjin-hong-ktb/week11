from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    email: EmailStr
    nickname: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    nickname: str
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None
    nickname: str | None
    password: str | None