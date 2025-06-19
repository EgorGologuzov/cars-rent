from sqlalchemy.orm import Session
from models import Review
from utils import HttpResponse
from schemas import Meta, Review_Create, Review_Update
from sqlalchemy import and_, or_, desc
from .car_usecases import Car_UseCases
from .user_usecases import User_UseCases


class Review_UseCases:

  def __init__(self, db: Session):
    self.db = db
    self.car_usecases = Car_UseCases(db)
    self.user_usecases = User_UseCases(db)


  def get_one(self, review_id, user_id=None):
    
    query = self.db.query(Review).filter(Review.id == review_id, Review.is_active)

    if user_id:
      query = query.filter(Review.user_id == user_id)

    review = query.first()

    if not review:
      raise HttpResponse.not_found("Отзыв не найден")

    Meta.deserialize_meta(review)

    return review


  def get_any(self, car_id=None, user_id=None, rating=None, page=None, limit=None):
    
    query = self.db.query(Review).filter(Review.is_active == True)

    page = page if page else 0
    limit = limit if limit else 100

    if car_id:
      query = query.filter(Review.car_id == car_id)
    if user_id:
      query = query.filter(Review.user_id == user_id)
    if rating:
      query = query.filter(Review.rating == rating)

    reviews = query.order_by(desc(Review.id)).offset(page * limit).limit(limit).all()
    Meta.deserialize_meta_foreach(reviews)

    return reviews


  def add_review(self, creator_id, create_data: Review_Create):
    
    search = self.get_any(car_id=create_data.car_id, user_id=creator_id)
    review = search[0] if len(search) > 0 else None

    if review:
      raise HttpResponse.bad_request("Вы уже оставили отзыв на этот автомобиль")
    
    car = self.car_usecases.get_one(create_data.car_id)
    user = self.user_usecases.get_one(creator_id)

    review = Review(**create_data.model_dump())
    review.user_id = creator_id
    Meta.add_meta(review, creator_id)

    self.db.rollback()
    self.db.add(review)
    self.db.commit()
    self.db.refresh(review)
    Meta.deserialize_meta(review)

    return review


  def update_review(self, updater_id, review_id, update_data: Review_Create):
    
    review = self.get_one(review_id, updater_id)

    for field, value in update_data.model_dump(exclude_unset=True).items():
      setattr(review, field, value)

    Meta.update_meta(review, updater_id)

    self.db.commit()
    self.db.refresh(review)
    Meta.deserialize_meta(review)

    return review


  def delete_review(self, updater_id, review_id, user_id=None):
    
    review = self.get_one(review_id, user_id)

    review.is_active = False
    Meta.update_meta(review, updater_id)

    self.db.commit()

    return HttpResponse.ok_message("Отзыв удален")

