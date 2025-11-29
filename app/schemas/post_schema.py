from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=26)
    content: str | None = Field(None, max_length=512)
    image_url: str | None = None
    

class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=26)
    content: str | None = Field(None, min_length=1)
    image_url: str | None = None


# 목록 조회용
class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    like_count: int
    view_count: int
    comment_count: int

    class Config:
        from_attributes = True
        
# 상세 조회용
class PostDetail(Post):
    # comments: List['Comment'] = []
    pass
