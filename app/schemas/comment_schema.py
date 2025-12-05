from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, description="댓글 내용")


class CommentCreate(CommentBase):
    post_id: int = Field(..., gt=0, description="게시글 ID")


class CommentUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1, description="댓글 내용")


class Comment(CommentBase):
    id: int = Field(description="댓글 ID")
    post_id: int = Field(description="게시글 ID")
    author_id: int = Field(description="작성자 ID")
    created_at: datetime = Field(description="생성 시간")

    model_config: ConfigDict = ConfigDict(from_attributes=True)