from sqlalchemy.orm import Session
from models import User
from utils import HttpResponse
from schemas import Meta
from auth import get_password_hash, verify_password, create_access_credentails
from schemas import SignInData, SignUpData, User_Update


class User_UseCases:

  def __init__(self, db: Session):
    self.db = db


  def get_one(self, user_id):

    user = self.db.query(User).filter(User.id == user_id, User.is_active).first()

    if not user:
      raise HttpResponse.not_found("Пользователь не найден")
    
    Meta.deserialize_meta(user)
  
    return user
  

  def get_any(self, email=None, full_name=None, role=None, page=None, limit=None):

    query = self.db.query(User).filter(User.is_active == True)

    page = page if page else 0
    limit = limit if limit else 100

    if email:
      query = query.filter(User.email == email)
    if full_name:
      query = query.filter(User.full_name == full_name)
    if role:
      query = query.filter(User.role == role)

    users = query.offset(page * limit).limit(limit).all()
    Meta.deserialize_meta_foreach(users)

    return users


  def sign_in(self, data: SignInData):

    email, password = data.email, data.password
    search = self.get_any(email=email)
    user = search[0] if len(search) > 0 else None

    if not user or not verify_password(password, user.hashed_password):
      raise HttpResponse.bad_request("Неверный логин или пароль")

    return create_access_credentails(user.id, user.role)


  def sign_up(self, creator_id, role, data: SignUpData):

    email, password = data.email, data.password
    search = self.get_any(email=email)
    user = search[0] if len(search) > 0 else None

    if user:
      raise HttpResponse.bad_request("Этот email уже занят другим пользователем")

    user = User(**data.model_dump(exclude={"password"}))
    user.role = role
    user.hashed_password = get_password_hash(password)
    Meta.add_meta(user, creator_id)

    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)

    return create_access_credentails(user.id, user.role)


  def update_user_data(self, updater_id, user_id, update_data: User_Update):
    
    search = self.get_any(email=update_data.email)
    found_by_email = search[0] if len(search) > 0 else None

    user = self.get_one(user_id)

    if found_by_email and found_by_email.email != user.email:
      raise HttpResponse.bad_request("Этот email уже занят другим пользователем")
    
    for field, value in update_data.model_dump(exclude={"password"}, exclude_unset=True).items():
      setattr(user, field, value)

    if update_data.password:
      user.hashed_password = get_password_hash(update_data.password)

    Meta.update_meta(user, updater_id)

    self.db.commit()
    self.db.refresh(user)
    Meta.deserialize_meta(user)

    return user


  def delete_user(self, updater_id, user_id):

    user = self.get_one(user_id)

    user.is_active = False
    Meta.update_meta(user, updater_id)

    self.db.commit()

    return HttpResponse.ok_message("Пользователь удален")

