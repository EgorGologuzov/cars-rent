from enum import Enum as Enum
from sqlalchemy import (Column, Integer, String, Boolean, Enum as SqlEnum)
from sqlalchemy.orm import relationship
from database import Base


class UserRole(str, Enum):
  CLIENT = "client"
  MANAGER = "manager"
  ADMIN = "admin"


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  is_active = Column(Boolean, default=True, nullable=False)
  email = Column(String(512), index=True, nullable=False)
  hashed_password = Column(String(256), nullable=False)
  full_name = Column(String(256), nullable=False)
  role = Column(SqlEnum(UserRole), nullable=False)

  meta = Column(String(1024), nullable=False)

  rentals = relationship("Rental", back_populates="user")
  reviews = relationship("Review", back_populates="user")

