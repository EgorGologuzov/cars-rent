from fastapi import APIRouter, Depends, Path, Query
from typing import List, Optional
from models import UserRole
from database import get_db
from usecases import User_UseCases
from schemas import AccessCredentials, SignInData, SignUpData, User_Return, User_Update, Message, TokenData
from pydantic import EmailStr
from auth import auth, PROTECTED_ENDPOINT_SECURITY


GUEST_USER_ID = -1


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

q_email = Query(
  default=None,
  description="Полный email пользователя",
  openapi_examples={
    "normal": {"value": "user@example.com"},
    "invalid": {"value": "notemail"},
  }
)

q_full_name = Query(
  default=None,
  max_length=256,
  description="Полное имя пользователя",
  openapi_examples={
    "normal": {"value": "Petr Petrov"},
  }
)

q_role = Query(
  default=None,
  description="Роль пользователя",
  openapi_examples={
    "normal": {"value": UserRole.CLIENT},
    "invalid": {"value": "fakerole"},
  }
)

p_role = Path(
  default=...,
  title="Роль пользователя",
  description="Роль пользователя, от нее зависит набор доступных функций",
  openapi_examples={
    "normal": {"value": UserRole.MANAGER},
    "invalid": {"value": "fakerole"},
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


def get_user_use_cases(db = Depends(get_db)):
  return User_UseCases(db)


@router.post(
  path="/user/sign/in",
  response_model=AccessCredentials,
  summary="Авторизация",
  tags=["Общий доступ"],
)
def sign_in(
  sign_in_data: SignInData,
  users: User_UseCases = Depends(get_user_use_cases),
):
  return users.sign_in(sign_in_data)


@router.post(
  path="/user/sign/up",
  response_model=AccessCredentials,
  summary="Регистрация клиента",
  tags=["Общий доступ"],
)
def sign_up_client(
  sign_up_data: SignUpData,
  users: User_UseCases = Depends(get_user_use_cases),
):
  return users.sign_up(GUEST_USER_ID, UserRole.CLIENT, sign_up_data)


@router.post(
  path="/a/users/sign/up/{role}",
  response_model=AccessCredentials,
  summary="Регистрация любой роли",
  tags=["Админ"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def sign_up_user(
  sign_up_data: SignUpData,
  role: UserRole = p_role,
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.ADMIN)),
):
  return users.sign_up(claims.user_id, role, sign_up_data)


@router.get(
  path="/a/users",
  response_model=List[User_Return],
  summary="Получение списка пользователей",
  tags=["Админ"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_users_for_admins(
  email: Optional[EmailStr] = q_email,
  full_name: Optional[str] = q_full_name,
  role: Optional[UserRole] = q_role,
  page: Optional[int] = q_page,
  limit: Optional[int] = q_limit,
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.ADMIN)),
):
  return users.get_any(email, full_name, role, page, limit)


@router.get(
  path="/a/users/{user_id}",
  response_model=User_Return,
  summary="Получение пользователя по id",
  tags=["Админ"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_user_for_admins(
  user_id: int = p_user_id,
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.ADMIN)),
):
  return users.get_one(user_id)


@router.get(
  path="/c/user",
  response_model=User_Return,
  summary="Получение своих данных пользователя",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_self_user_data_for_client(
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return users.get_one(claims.user_id)


@router.get(
  path="/m/user",
  response_model=User_Return,
  summary="Получение своих данных пользователя",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def get_self_user_data_for_manager(
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return users.get_one(claims.user_id)


@router.put(
  path="/c/user",
  response_model=User_Return,
  summary="Обновление данных своего аккаунта",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def update_user_client(
  user_data: User_Update,
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return users.update_user_data(claims.user_id, claims.user_id, user_data)


@router.put(
  path="/m/user",
  response_model=User_Return,
  summary="Обновление данных своего аккаунта",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def update_user_manager(
  user_data: User_Update,
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return users.update_user_data(claims.user_id, claims.user_id, user_data)


@router.put(
  path="/a/users/{user_id}",
  response_model=User_Return,
  summary="Обновление данных любого аккаунта",
  tags=["Админ"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def update_user_admin(
  user_data: User_Update,
  user_id: int = p_user_id,
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.ADMIN)),
):
  return users.update_user_data(claims.user_id, user_id, user_data)


@router.delete(
  path="/c/user",
  response_model=Message,
  summary="Удаление своего аккаунта",
  tags=["Клиент"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def delete_user_client(
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.CLIENT)),
):
  return users.delete_user(claims.user_id, claims.user_id)


@router.delete(
  path="/m/user",
  response_model=Message,
  summary="Удаление своего аккаунтата",
  tags=["Менеджер"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def delete_user_manager(
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.MANAGER)),
):
  return users.delete_user(claims.user_id, claims.user_id)


@router.delete(
  path="/a/users/{user_id}",
  response_model=Message,
  summary="Удаление любого аккаунта",
  tags=["Админ"],
  openapi_extra={"security": PROTECTED_ENDPOINT_SECURITY},
)
def delete_user_admin(
  user_id: int = p_user_id,
  users: User_UseCases = Depends(get_user_use_cases),
  claims: TokenData = Depends(auth(UserRole.ADMIN)),
):
  return users.delete_user(claims.user_id, user_id)

