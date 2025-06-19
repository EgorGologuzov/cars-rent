from fastapi import APIRouter, Depends, Path, Query
from typing import List, Optional
from schemas import Review_Return, Review_Create, Message, Review_Update
from models import UserRole
from database import get_db
from usecases import Review_UseCases
from schemas import TokenData
from auth import auth, PROTECTED_ENDPOINT_SECURITY
from datetime import datetime, timezone, timedelta, date


router = APIRouter()


q_page = Query(
  default=0,
  ge=0,
  description="Номер страницы пейджинга (положительное число)",
  openapi_examples={
    "normal": {"value": 1},
    "invalid": {"value": -1},
  }
)

q_limit = Query(
  default=100,
  le=100,
  description="Максимальное кол-во сущностей в ответе (максимум 100)",
  openapi_examples={
    "normal": {"value": 3},
    "invalid": {"value": 101},
  }
)


q_car_id = Query(
  default=None,
  description="Уникальный id автомобиля (целое число)",
  openapi_examples={
    "normal": {"value": 1},
    "invalid": {"value": "NaN"},
  }
)

q_user_id = Query(
  default=None,
  description="Уникальный id пользователя (целое число)",
  openapi_examples={
    "normal": {"value": 3},
    "invalid": {"value": "NaN"},
  }
)

q_rating = Query(
  default=None,
  description="Оценка автомобиля по шкале от 1 до 5 (целое число)",
  openapi_examples={
    "normal": {"value": 5},
    "invalid": {"value": "NaN"},
  }
)

p_review_id = Path(
  default=...,
  title="Id отзыва",
  description="Уникальный id отзыва (целое число)",
  openapi_examples={
    "normal": {"value": 1},
    "invalid": {"value": "NaN"},
  }
)


def get_review_use_cases(db = Depends(get_db)):
  return Review_UseCases(db)


@router.get(
  path="/c/reviews",
  response_model=List[Review_Return],
  summary="Получение списка своих отзывов",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_reviews_for_client(
  reviews: Review_UseCases = Depends(get_review_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
  car_id: Optional[int] = q_car_id,
  rating: Optional[int] = q_rating,
  page: Optional[int] = q_page,
  limit: Optional[int] = q_limit,
):
  return reviews.get_any(car_id, claims.user_id, rating, page, limit)


@router.get(
  path="/a/reviews",
  response_model=List[Review_Return],
  summary="Получение списка любых отзывов",
  tags=["Админ"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_reviews_for_admin(
  reviews: Review_UseCases = Depends(get_review_use_cases),
  claims: TokenData = Depends(auth(UserRole.ADMIN)),
  car_id: Optional[int] = q_car_id,
  user_id: Optional[int] = q_user_id,
  rating: Optional[int] = q_rating,
  page: Optional[int] = q_page,
  limit: Optional[int] = q_limit,
):
  return reviews.get_any(car_id, user_id, rating, page, limit)


@router.get(
  path="/c/reviews/{review_id}",
  response_model=Review_Return,
  summary="Получение своего отзыва по id",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_review_for_client(
  reviews: Review_UseCases = Depends(get_review_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
  review_id: int = p_review_id,
):
  return reviews.get_one(review_id, claims.user_id)


@router.get(
  path="/a/reviews/{review_id}",
  response_model=Review_Return,
  summary="Получение любого отзыва по id",
  tags=["Админ"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_review_for_admin(
  reviews: Review_UseCases = Depends(get_review_use_cases),
  claims: TokenData = Depends(auth(UserRole.ADMIN)),
  review_id: int = p_review_id,
):
  return reviews.get_one(review_id)


@router.post(
  path="/c/reviews",
  response_model=Review_Return,
  summary="Создание отзыва",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def add_review(
  create_data: Review_Create,
  reviews: Review_UseCases = Depends(get_review_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return reviews.add_review(claims.user_id, create_data)


@router.put(
  path="/c/reviews/{review_id}",
  response_model=Review_Return,
  summary="Обновление своего отзыва",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def update_review(
  update_data: Review_Update,
  review_id: int = p_review_id,
  reviews: Review_UseCases = Depends(get_review_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return reviews.update_review(claims.user_id, review_id, update_data)


@router.delete(
  path="/c/reviews/{review_id}",
  response_model=Message,
  summary="Удаление своего отзыва",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def delete_review_for_client(
  review_id: int = p_review_id,
  reviews: Review_UseCases = Depends(get_review_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return reviews.delete_review(claims.user_id, review_id, claims.user_id)


@router.delete(
  path="/a/reviews/{review_id}",
  response_model=Message,
  summary="Удаление любого отзыва",
  tags=["Админ"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def delete_review_for_admin(
  review_id: int = p_review_id,
  reviews: Review_UseCases = Depends(get_review_use_cases),
  claims: TokenData = Depends(auth(UserRole.ADMIN)),
):
  return reviews.delete_review(claims.user_id, review_id)

