from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .meta_schemas import Meta
from models import CarType, CarStatus


# f - field; rf - required field
f_brand = Field(None, min_length=2, max_length=128, example="Toyota")
f_model = Field(None, min_length=2, max_length=128, example="Camry")
f_year = Field(None, gt=1900, example=2022)
f_type = Field(None, example=CarType.SEDAN)
rf_price_per_day = Field(..., gt=0, example=500.0)
f_price_per_day = Field(None, gt=0, example=500.0)
rf_status = Field(..., example=CarStatus.RENTED)
f_status = Field(None, example=CarStatus.RENTED)


class Car_ReturnForClients(BaseModel):
  id: int
  brand: str | None
  model: str | None
  year: int | None
  type: CarType | None
  price_per_day: float
  status: CarStatus


class Car_ReturnForEmployees(BaseModel):
  id: int
  brand: str | None
  model: str | None
  year: int | None
  type: CarType | None
  price_per_day: float
  status: CarStatus
  meta: Meta

  model_config = ConfigDict(
    arbitrary_types_allowed=True
  )


class Car_Create(BaseModel):
  brand: Optional[str] = f_brand
  model: Optional[str] = f_model
  year: Optional[int] = f_year
  type: Optional[CarType] = f_type
  price_per_day: float = rf_price_per_day
  status: CarStatus = rf_status


class Car_Update(BaseModel):
  brand: Optional[str] = f_brand
  model: Optional[str] = f_model
  year: Optional[int] = f_year
  type: Optional[CarType] = f_type
  price_per_day: Optional[float] = f_price_per_day
  status: Optional[CarStatus] = f_status

