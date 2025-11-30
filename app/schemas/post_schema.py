from pydantic import BaseModel, Field
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.comment_schema import Comment


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    image_url: str | None = None


class PostCreate(PostBase):
    # created_at: datetime = datetime.now()
    pass


class PostUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    content: str | None = Field(None, min_length=1)
    image_url: str | None = None


# 목록 조회용
class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    like_count: int
    view_count: int

    class Config:
        from_attributes = True


# 상세 조회용 (댓글 포함)
class PostDetail(Post):
    comments: List["Comment"] = []


# 순환 import 해결을 위해 런타임에 Comment 임포트 후 모델 재빌드
from app.schemas.comment_schema import Comment
PostDetail.model_rebuild()
