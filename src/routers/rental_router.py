from fastapi import APIRouter, Depends, Path, Query
from typing import List, Optional
from schemas import Rental_Return, Rental_Create, Message, Rental_ReturnIn_Schedule, Rental_TotalCost
from models import RentalStatus, UserRole
from database import get_db
from usecases import Rental_UseCases
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

q_period_start = Query(
  default=None,
  description="Начальная дата периода. Фильтр пройдут все записы период которых пересекается с заданным периодом.",
  openapi_examples={
    "normal": {"value": (datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat()},
    "invalid": {"value": "2024-08-0104:39:06"},
  }
)

q_period_end = Query(
  default=None,
  description="Конечная дата периода. Фильтр пройдут все записы период которых пересекается с заданным периодом.",
  openapi_examples={
    "normal": {"value": (datetime.now(timezone.utc) + timedelta(days=10)).date().isoformat()},
    "invalid": {"value": "2024-08-0104:39:06"},
  }
)

q_status = Query(
  default=None,
  description=f"Статус арнеды",
  openapi_examples={
    "normal": {"value": RentalStatus.ACTIVE},
    "invalid": {"value": "fakestatus"},
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

p_rental_id = Path(
  default=...,
  title="Id арнеды",
  description="Уникальный id аренды (целое число)",
  openapi_examples={
    "normal": {"value": 1},
    "invalid": {"value": "NaN"},
  }
)

p_user_id = Path(
  default=...,
  title="Id пользователя",
  description="Уникальный id пользователя (целое число)",
  openapi_examples={
    "normal": {"value": 1},
    "invalid": {"value": "NaN"},
  }
)

p_status = Path(
  default=...,
  description="Статус арнеды",
  openapi_examples={
    "normal": {"value": RentalStatus.ACTIVE},
    "invalid": {"value": "fakestatus"},
  }
)

rq_car_id = Query(
  default=...,
  description="Уникальный id автомобиля (целое число)",
  openapi_examples={
    "normal": {"value": 1},
    "invalid": {"value": "NaN"},
  }
)

rq_period_start = Query(
  default=...,
  description="Начальная дата периода. Фильтр пройдут все записы период которых пересекается с заданным периодом.",
  openapi_examples={
    "normal": {"value": (datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat()},
    "invalid": {"value": "2024-08-0104:39:06"},
  }
)

rq_period_end = Query(
  default=...,
  description="Конечная дата периода. Фильтр пройдут все записы период которых пересекается с заданным периодом.",
  openapi_examples={
    "normal": {"value": (datetime.now(timezone.utc) + timedelta(days=10)).date().isoformat()},
    "invalid": {"value": "2024-08-0104:39:06"},
  }
)

def get_rental_use_cases(db = Depends(get_db)):
  return Rental_UseCases(db)


@router.get(
  path="/c/rentals",
  response_model=List[Rental_Return],
  summary="Получение списка своих аренд",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_rentals_for_client(
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
  car_id: Optional[int] = q_car_id,
  status: Optional[RentalStatus] = q_status,
  page: Optional[int] = q_page,
  limit: Optional[int] = q_limit,
):
  return rentals.get_any(car_id=car_id, user_id=claims.user_id, status=status, page=page, limit=limit)


@router.get(
  path="/c/rentals/schedule",
  response_model=List[Rental_ReturnIn_Schedule],
  summary="Получение расписания автомобиля за период",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_cars_schedule_for_client(
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
  car_id: int = rq_car_id,
  period_start: date = rq_period_start,
  period_end: date = rq_period_end,
):
  return rentals.get_any(car_id=car_id, period_start=period_start, period_end=period_end)


@router.get(
  path="/m/rentals",
  response_model=List[Rental_Return],
  summary="Получение списка любых аренд",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_rentals_for_manager(
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
  car_id: Optional[int] = q_car_id,
  user_id: Optional[int] = q_user_id,
  status: Optional[RentalStatus] = q_status,
  period_start: date = q_period_start,
  period_end: date = q_period_end,
  page: Optional[int] = q_page,
  limit: Optional[int] = q_limit,
):
  return rentals.get_any(car_id=car_id, user_id=user_id, status=status, period_start=period_start, period_end=period_end, page=page, limit=limit)


@router.get(
  path="/m/rentals/schedule",
  response_model=List[Rental_Return],
  summary="Получение расписания автомобиля за период",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_cars_schedule_for_manager(
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
  car_id: Optional[int] = rq_car_id,
  period_start: Optional[date] = rq_period_start,
  period_end: Optional[date] = rq_period_end,
):
  return rentals.get_any(car_id=car_id, period_start=period_start, period_end=period_end)


@router.get(
  path="/c/rentals/{rental_id}",
  response_model=Rental_Return,
  summary="Получение своей аренды по id",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_rental_for_client(
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
  rental_id: int = p_rental_id,
):
  return rentals.get_one(rental_id, claims.user_id)


@router.get(
  path="/m/rentals/{rental_id}",
  response_model=Rental_Return,
  summary="Получение любой аренды по id",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_rental_for_manager(
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
  rental_id: int = p_rental_id,
):
  return rentals.get_one(rental_id)


@router.post(
  path="/c/rentals/calc/total/cost",
  response_model=Rental_TotalCost,
  summary="Расчет стоимости аренды авто за период",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def calc_rental_total_cost_for_client(
  rental_data: Rental_Create,
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return rentals.get_rental_total_cost(rental_data)


@router.post(
  path="/m/rentals/calc/total/cost",
  response_model=Rental_TotalCost,
  summary="Расчет стоимости аренды авто за период",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def calc_rental_total_cost_for_manager(
  rental_data: Rental_Create,
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return rentals.get_rental_total_cost(rental_data)


@router.post(
  path="/c/rentals",
  response_model=Rental_Return,
  summary="Бронирование авто для себя",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def create_rental_for_client(
  rental_data: Rental_Create,
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return rentals.create_rental(claims.user_id, claims.user_id, rental_data)


@router.post(
  path="/m/rentals/for/{user_id}",
  response_model=Rental_Return,
  summary="Бронирование авто для любого пользователя",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def create_rental_for_manager(
  rental_data: Rental_Create,
  user_id: int = p_user_id,
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return rentals.create_rental(claims.user_id, user_id, rental_data)


@router.patch(
  path="/c/rentals/{rental_id}/cancel",
  response_model=Rental_Return,
  summary="Отмена аренды",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def cancel_clients_rental(
  rental_id: int = p_rental_id,
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return rentals.update_rental_status(claims.user_id, RentalStatus.CANCELLED, rental_id, claims.user_id)


@router.patch(
  path="/m/rentals/{rental_id}/status/{status}",
  response_model=Rental_Return,
  summary="Изменение статуса аренды (отмена, завершение, передача авто клиенту)",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def change_rental_status(
  rental_id: int = p_rental_id,
  status: RentalStatus = p_status,
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return rentals.update_rental_status(claims.user_id, status, rental_id)


@router.delete(
  path="/m/rentals/{rental_id}",
  response_model=Message,
  summary="Удаление аренды",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def delete_rental(
  rental_id: int = p_rental_id,
  rentals: Rental_UseCases = Depends(get_rental_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return rentals.delete_rental(claims.user_id, rental_id)

