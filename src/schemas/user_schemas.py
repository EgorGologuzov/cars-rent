from pydantic import BaseModel, EmailStr, Field
from models import UserRole
from .meta_schemas import Meta
from datetime import datetime


# f - field; rf - required field
f_email = Field(None, min_length=1, max_length=512, example="user@example.com")
rf_email = Field(..., min_length=1, max_length=512, example="user@example.com")
f_full_name = Field(None, min_length=1, max_length=256, example="John Doe")
rf_full_name = Field(..., min_length=1, max_length=256, example="John Doe")
f_password = Field(None, min_length=8, max_length=256, example="12345678")
rf_password = Field(..., min_length=8, max_length=256, example="12345678")
f_role = Field(None, example=UserRole.CLIENT)


class User_Return(BaseModel):
  id: int
  email: EmailStr = f_email
  full_name: str = f_full_name
  role: UserRole = f_role
  meta: Meta


class User_Update(BaseModel):
  email: EmailStr = f_email
  full_name: str = f_full_name
  password: str = f_password


class AccessCredentials(BaseModel):
  access_token: str
  token_type: str
  expiring_at: datetime


class TokenData(BaseModel):
  user_id: int
  user_role: UserRole = f_role


class SignInData(BaseModel):
  email: EmailStr = rf_email
  password: str = rf_password


class SignUpData(BaseModel):
  email: EmailStr = rf_email
  full_name: str = rf_full_name
  password: str = rf_password


class User_ReturnIn_Rental(BaseModel):
  id: int
  email: str = rf_email
  full_name: str = f_full_name

