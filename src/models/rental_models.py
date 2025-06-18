from enum import Enum as Enum
from sqlalchemy import (Column, Integer, Float, ForeignKey, String, DateTime, Boolean, Enum as SqlEnum)
from sqlalchemy.orm import relationship
from database import Base


class RentalStatus(str, Enum):
  ACTIVE = "active"             # офромлена
  PENDING = "pending"           # клиент пользуется машиной
  COMPLETED = "completed"       # завершена
  CANCELLED = "cancelled"       # отменена


class Rental(Base):
  __tablename__ = "rentals"

  id = Column(Integer, primary_key=True, index=True)
  is_active = Column(Boolean, default=True, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
  start_date = Column(DateTime, nullable=False)
  end_date = Column(DateTime, nullable=False)
  total_cost = Column(Float, nullable=False)
  status = Column(SqlEnum(RentalStatus), default=RentalStatus.ACTIVE, nullable=False)

  meta = Column(String(1024), nullable=False)

  user = relationship("User", back_populates="rentals")
  car = relationship("Car", back_populates="rentals")

