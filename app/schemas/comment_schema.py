from pydantic import BaseModel, Field
from datetime import datetime


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str | None = Field(None, min_length=1)


class Comment(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True