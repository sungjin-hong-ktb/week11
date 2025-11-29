from sqlalchemy import Column, Integer, String

from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)