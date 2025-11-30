from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    # 외래키: 게시글
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    # 외래키: 작성자
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # 관계
    post = relationship("Post", back_populates="comments")
    author = relationship("Users", back_populates="comments")
