from fastapi import APIRouter, Depends, Path, Query
from typing import List, Optional
from schemas import Car_ReturnFor_Client, Car_ReturnFor_Manager, Car_Create, Car_Update, Message
from models import CarType, CarStatus
from database import get_db
from usecases import Car_UseCases
from schemas import TokenData
from models import UserRole
from auth import auth, PROTECTED_ENDPOINT_SECURITY


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

q_type = Query(
  default=None,
  description=f"Тип автомобиля",
  openapi_examples={
    "normal": {"value": CarType.SEDAN},
    "invalid": {"value": "faketype"},
  }
)

q_status = Query(
  default=None,
  description=f"Статус автомобиля",
  openapi_examples={
    "normal": {"value": CarStatus.AVAILABLE},
    "invalid": {"value": "fakestatus"},
  }
)

q_min_year = Query(
  default=None,
  description=f"Минимальный год выпуска",
  openapi_examples={
    "normal": {"value": 2022},
  }
)

p_car_id = Path(
  default=...,
  title="Id автомобиля",
  description="Уникальный id автомобиля (целое число)",
  openapi_examples={
    "normal": {"value": 1},
    "invalid": {"value": "NaN"},
  }
)


def get_car_use_cases(db = Depends(get_db)):
  return Car_UseCases(db)


@router.get(
  path="/c/cars",
  response_model=List[Car_ReturnFor_Client],
  summary="Получение списка автомобилей",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_cars_for_clients(
  cars: Car_UseCases = Depends(get_car_use_cases),
  type: Optional[CarType] = q_type,
  status: Optional[CarStatus] = q_status,
  min_year: Optional[int] = q_min_year,
  page: Optional[int] = q_page,
  limit: Optional[int] = q_limit,
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return cars.get_any(type, status, min_year, page, limit)


@router.get(
  path="/c/cars/{car_id}",
  response_model=Car_ReturnFor_Client,
  summary="Получение автомобиля по id",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_car_for_clients(
  cars: Car_UseCases = Depends(get_car_use_cases),
  car_id: int = p_car_id,
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return cars.get_one(car_id)



@router.get(
  path="/m/cars",
  response_model=List[Car_ReturnFor_Manager],
  summary="Получение списка автомобилей",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_cars_for_managers(
  cars: Car_UseCases = Depends(get_car_use_cases),
  type: Optional[CarType] = q_type,
  status: Optional[CarStatus] = q_status,
  min_year: Optional[int] = q_min_year,
  page: Optional[int] = q_page,
  limit: Optional[int] = q_limit,
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return cars.get_any(type, status, min_year, page, limit)


@router.get(
  path="/m/cars/{car_id}",
  response_model=Car_ReturnFor_Manager,
  summary="Получение автомобиля по id",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_car_for_managar(
  cars: Car_UseCases = Depends(get_car_use_cases),
  car_id: int = p_car_id,
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return cars.get_one(car_id)


@router.post(
  path="/m/cars",
  response_model=Car_ReturnFor_Manager,
  summary="Добавление автомобиля",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def add_car(
  car_data: Car_Create,
  cars: Car_UseCases = Depends(get_car_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return cars.add_car(claims.user_id, car_data)


@router.put(
  path="/m/cars/{car_id}",
  response_model=Car_ReturnFor_Manager,
  summary="Обновление данных автомобиля",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def update_car(
  car_data: Car_Update,
  car_id: int = p_car_id,
  cars: Car_UseCases = Depends(get_car_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return cars.update_car(claims.user_id, car_id, car_data)


@router.delete(
  path="/m/cars/{car_id}",
  response_model=Message,
  summary="Удаление автомобиля",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def delete_car(
  car_id: int = p_car_id,
  cars: Car_UseCases = Depends(get_car_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return cars.delete_car(claims.user_id, car_id)

