from fastapi import APIRouter, Depends, Path, Query
from typing import List, Optional
from schemas import Car_ReturnForClients, Car_ReturnForEmployees, Car_Create, Car_Update, Message
from models import CarType, CarStatus
from database import get_db
from usecases import Car_UseCases


router = APIRouter()


f_page = Query(
  default=0,
  ge=0,
  description="Номер страницы пейджинга (положительное число)",
  openapi_examples={
    "normal": {"value": 1},
    "invalid": {"value": -1},
  }
)

f_limit = Query(
  default=100,
  le=100,
  description="Максимальное кол-во сущностей в ответе (максимум 100)",
  openapi_examples={
    "normal": {"value": 3},
    "invalid": {"value": 101},
  }
)

f_type = Query(
  default=None,
  description=f"Тип автомобиля",
  openapi_examples={
    "normal": {"value": CarType.SEDAN},
    "invalid": {"value": "faketype"},
  }
)

f_status = Query(
  default=None,
  description=f"Статус автомобиля",
  openapi_examples={
    "normal": {"value": CarStatus.AVAILABLE},
    "invalid": {"value": "fakestatus"},
  }
)

f_min_year = Query(
  default=None,
  description=f"Минимальный год выпуска",
  openapi_examples={
    "normal": {"value": 2022},
  }
)

f_car_id = Path(
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
  response_model=List[Car_ReturnForClients],
  summary="Получение списка автомобилей",
  tags=["Клиент"],
)
def get_cars_for_clients(
  cars: Car_UseCases = Depends(get_car_use_cases),
  type: Optional[CarType] = f_type,
  status: Optional[CarStatus] = f_status,
  min_year: Optional[int] = f_min_year,
  page: Optional[int] = f_page,
  limit: Optional[int] = f_limit,
):
  return cars.get_any(type, status, min_year, page, limit)


@router.get(
  path="/c/cars/{car_id}",
  response_model=Car_ReturnForClients,
  summary="Получение автомобиля по id",
  tags=["Клиент"],
)
def get_car_for_clients(
  cars: Car_UseCases = Depends(get_car_use_cases),
  car_id: int = f_car_id,
):
  return cars.get_one(car_id)



@router.get(
  path="/m/cars",
  response_model=List[Car_ReturnForEmployees],
  summary="Получение списка автомобилей",
  tags=["Менеджер"],
)
def get_cars_for_managers(
  cars: Car_UseCases = Depends(get_car_use_cases),
  type: Optional[CarType] = f_type,
  status: Optional[CarStatus] = f_status,
  min_year: Optional[int] = f_min_year,
  page: Optional[int] = f_page,
  limit: Optional[int] = f_limit,
):
  return cars.get_any(type, status, min_year, page, limit)


@router.get(
  path="/m/cars/{car_id}",
  response_model=Car_ReturnForEmployees,
  summary="Получение автомобиля по id",
  tags=["Менеджер"],
)
def get_car_for_managar(
  cars: Car_UseCases = Depends(get_car_use_cases),
  car_id: int = f_car_id,
):
  return cars.get_one(car_id)


@router.get(
  path="/a/cars",
  response_model=List[Car_ReturnForEmployees],
  summary="Получение списка автомобилей",
  tags=["Админ"],
)
def get_cars_for_admins(
  cars: Car_UseCases = Depends(get_car_use_cases),
  type: Optional[CarType] = f_type,
  status: Optional[CarStatus] = f_status,
  min_year: Optional[int] = f_min_year,
  page: Optional[int] = f_page,
  limit: Optional[int] = f_limit,
):
  return cars.get_any(type, status, min_year, page, limit)


@router.get(
  path="/a/cars/{car_id}",
  response_model=Car_ReturnForEmployees,
  summary="Получение автомобиля по id",
  tags=["Админ"],
)
def get_car_for_admins(
  cars: Car_UseCases = Depends(get_car_use_cases),
  car_id: int = f_car_id,
):
  return cars.get_one(car_id)


@router.post(
  path="/m/cars",
  response_model=Car_ReturnForEmployees,
  summary="Добавление автомобиля",
  tags=["Менеджер"],
)
def add_car(
  car_data: Car_Create,
  cars: Car_UseCases = Depends(get_car_use_cases),
):
  return cars.add_car(**car_data.model_dump())


@router.put(
  path="/m/cars/{car_id}",
  response_model=Car_ReturnForEmployees,
  summary="Обновление данных автомобиля",
  tags=["Менеджер"],
)
def update_car(
  car_data: Car_Update,
  car_id: int = f_car_id,
  cars: Car_UseCases = Depends(get_car_use_cases),
):
  return cars.update_car(car_id, **car_data.model_dump(exclude_unset=True))


@router.delete(
  path="/m/cars/{car_id}",
  response_model=Message,
  summary="Удаление автомобиля из базы данных",
  tags=["Менеджер"],
)
def delete_car(
  car_id: int = f_car_id,
  cars: Car_UseCases = Depends(get_car_use_cases),
):
  return cars.delete_car(car_id)

