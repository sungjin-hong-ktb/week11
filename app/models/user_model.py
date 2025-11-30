from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # 관계: 게시글들과 댓글들 (passive_deletes로 DB CASCADE에 맡김)
    posts = relationship("Post", back_populates="author", passive_deletes=True)
    comments = relationship("Comment", back_populates="author", passive_deletes=True)