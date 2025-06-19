from datetime import datetime, date, timedelta, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models import RentalStatus
from .car_schemas import Car_ReturnIn_Rental
from .user_schemas import User_ReturnIn_Rental
from .meta_schemas import Meta


# f - field; rf - required field
f_user_id = Field(None, gt=0, example=1)
rf_user_id = Field(..., gt=0, example=1)
f_car_id = Field(None, gt=0, example=1)
rf_car_id = Field(..., gt=0, example=1)
f_start_date = Field(None, example=(datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat())
rf_start_date = Field(..., example=(datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat())
f_end_date = Field(None, example=(datetime.now(timezone.utc) + timedelta(days=10)).date().isoformat())
rf_end_date = Field(..., example=(datetime.now(timezone.utc) + timedelta(days=10)).date().isoformat())
f_total_cost = Field(None, gt=0, example=1000.0)
rf_total_cost = Field(..., gt=0, example=1000.0)
f_status = Field(None, example=RentalStatus.ACTIVE)
rf_status = Field(default=RentalStatus.PENDING, example=RentalStatus.ACTIVE)


class Rental_Return(BaseModel):
  id: int
  start_date: date = f_start_date
  end_date: date = f_end_date
  total_cost: float = f_total_cost
  status: RentalStatus = f_status
  car: Car_ReturnIn_Rental
  user: User_ReturnIn_Rental
  meta: Meta


class Rental_ReturnIn_Schedule(BaseModel):
  id: int
  car_id: int = rf_car_id
  start_date: date = f_start_date
  end_date: date = f_end_date
  status: RentalStatus = f_status


class Rental_Create(BaseModel):
  car_id: int = rf_car_id
  start_date: date = rf_start_date
  end_date: date = rf_end_date


class Rental_TotalCost(BaseModel):
  total_cost: float = rf_total_cost
  full_cost: float
  message: Optional[str]

