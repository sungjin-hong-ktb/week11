from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now().replace(microsecond=0), nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    # 외래키: 작성자
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # 관계: 댓글들
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    # 관계: 작성자
    author = relationship("Users", back_populates="posts")