from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from schemas import TokenData, AccessCredentials
from utils import HttpResponse
from models import UserRole


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)


SECRET_KEY = "04f02588de78e294beac8395e67e1fd886a70eab41595edd0f149030f578a0c6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
PROTECTED_ENDPOINT_SECURITY = [{"BearerAuth": []}]


oauth2_scheme = OAuth2PasswordBearer(
  tokenUrl="/api/user/sign/in",
  scheme_name="Bearer",
  auto_error=False,
)


def create_access_credentails(id, role):

  expiring_at = datetime.now(timezone.utc) + \
      timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  token_data = {
      "id": id,
      "role": role,
      "exp": expiring_at,
  }

  token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

  return AccessCredentials(
      access_token=token,
      token_type="bearer",
      expiring_at=expiring_at,
  )


def auth(accessed_role: UserRole = None):
  def auth_inner(token: str = Depends(oauth2_scheme)):

    if not token:
      raise HttpResponse.unauthorized()

    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
      raise HttpResponse.unauthorized()

    id = payload.get("id")
    role = payload.get("role")

    if accessed_role and role != accessed_role:
      raise HttpResponse.forbidden()

    return TokenData(
      user_id=id,
      user_role=role,
    )
  
  return auth_inner
