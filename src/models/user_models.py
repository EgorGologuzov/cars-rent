from enum import Enum as Enum
from sqlalchemy import (Column, Integer, String, Enum as SqlEnum)
from sqlalchemy.orm import relationship
from database import Base
from auth import verify_password


class UserRole(str, Enum):
  CLIENT = "client"
  MANAGER = "manager"
  ADMIN = "admin"


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String(512), unique=True, index=True, nullable=False)
  hashed_password = Column(String(256), nullable=False)
  full_name = Column(String(256), nullable=False)
  role = Column(SqlEnum(UserRole), nullable=False)

  meta = Column(String(1024), nullable=False)

  rentals = relationship("Rental", back_populates="user")
  reviews = relationship("Review", back_populates="user")

  def verify_password(self, password: str) -> bool:
    return verify_password(password, self.hashed_password)

