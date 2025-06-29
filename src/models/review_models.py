from sqlalchemy import (Column, Integer, String, ForeignKey, Boolean)
from sqlalchemy.orm import relationship
from database import Base


class Review(Base):
  __tablename__ = "reviews"

  id = Column(Integer, primary_key=True, index=True)
  is_active = Column(Boolean, default=True, nullable=False)
  car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  rating = Column(Integer, nullable=False)
  comment = Column(String(2048), nullable=False)

  meta = Column(String(1024), nullable=False)

  car = relationship("Car", back_populates="reviews")
  user = relationship("User", back_populates="reviews")

