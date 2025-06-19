from pydantic import BaseModel, Field
from typing import Optional
from .meta_schemas import Meta


# f - field; rf - required field
rf_car_id = Field(..., example=1)
rf_user_id = Field(..., example=3)
rf_rating = Field(..., ge=1, le=5, example=4)
f_rating = Field(None, ge=1, le=5, example=4)
rf_comment = Field(..., min_length=2, max_length=2000, example="Отличный автомобиль, всем рекомендую!")
f_comment = Field(None, min_length=2, max_length=2000, example="Отличный автомобиль, всем рекомендую!")


class Review_Return(BaseModel):
  id: int
  car_id: int = rf_car_id
  user_id: int = rf_user_id
  rating: int = rf_rating
  comment: str = rf_comment
  meta: Meta


class Review_Create(BaseModel):
  car_id: int = rf_car_id
  rating: int = rf_rating
  comment: str = rf_comment


class Review_Update(BaseModel):
  rating: Optional[int] = f_rating
  comment: Optional[str] = f_comment

