from pydantic import BaseModel, Field, ConfigDict
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.comment_schema import Comment


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="게시글 제목")
    content: str = Field(..., min_length=1, description="게시글 내용")
    image_url: str | None = Field(default=None, description="이미지 URL")


class PostCreate(PostBase):
    pass  # author_id는 Header로 전달


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100, description="게시글 제목")
    content: str | None = Field(default=None, min_length=1, description="게시글 내용")
    image_url: str | None = Field(default=None, description="이미지 URL")


class Post(PostBase):
    id: int = Field(description="게시글 ID")
    author_id: int = Field(gt=0, description="작성자 ID")
    created_at: datetime = Field(description="생성 시간")
    like_count: int = Field(default=0, ge=0, description="좋아요 수")
    view_count: int = Field(default=0, ge=0, description="조회수")
    comment_count: int = Field(default=0, ge=0, description="댓글 수")

    model_config: ConfigDict = ConfigDict(from_attributes=True)


# 상세 조회용 (댓글 포함)
class PostDetail(Post):
    comments: List["Comment"] = Field(default=[], description="댓글 목록")


# 순환 import 해결을 위해 런타임에 Comment 임포트 후 모델 재빌드
from app.schemas.comment_schema import Comment
PostDetail.model_rebuild()
