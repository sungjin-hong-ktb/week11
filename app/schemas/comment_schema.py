from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    post_id: int = Field(..., description="게시글 ID")


class CommentUpdate(BaseModel):
    content: str | None = Field(None, min_length=1)


class Comment(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime

    model_config: ConfigDict = ConfigDict(from_attributes=True)