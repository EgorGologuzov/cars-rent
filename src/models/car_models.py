from enum import Enum
from sqlalchemy import (Column, Integer, String, Float, Enum as SqlEnum)
from sqlalchemy.orm import relationship
from database import Base


class CarType(str, Enum):
  SEDAN = "sedan"
  SUV = "suv"
  HATCHBACK = "hatchback"
  COUPE = "coupe"
  CONVERTIBLE = "convertible"
  OTHER = "other"


class CarStatus(str, Enum):
  AVAILABLE = "available"         # доступна
  RENTED = "rented"               # забронирована
  MAINTENANCE = "maintenance"     # на обслуживании


class Car(Base):
  __tablename__ = "cars"

  id = Column(Integer, primary_key=True, index=True)
  brand = Column(String(128), index=True)
  model = Column(String(128), index=True)
  year = Column(Integer)
  type = Column(SqlEnum(CarType))
  price_per_day = Column(Float, nullable=False)
  status = Column(SqlEnum(CarStatus), default=CarStatus.AVAILABLE, nullable=False)

  meta = Column(String(1024), nullable=False)

  rentals = relationship("Rental", back_populates="car")
  reviews = relationship("Review", back_populates="car")

