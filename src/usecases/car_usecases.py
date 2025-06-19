from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Car
from utils import HttpResponse
from schemas import Meta, Car_Create, Car_Update


class Car_UseCases:

  def __init__(self, db: Session):
    self.db = db


  def get_one(self, car_id):

    car = self.db.query(Car).filter(Car.id == car_id, Car.is_active).first()

    if not car:
      raise HttpResponse.not_found("Автомобиль не найден")
    
    Meta.deserialize_meta(car)
  
    return car
  

  def get_any(self, type=None, status=None, min_year=None, page=None, limit=None):

    query = self.db.query(Car).filter(Car.is_active == True)

    page = page if page else 0
    limit = limit if limit else 100

    if type:
      query = query.filter(Car.type == type)
    if status:
      query = query.filter(Car.status == status)
    if min_year:
      query = query.filter(Car.year >= min_year)

    cars = query.order_by(desc(Car.id)).offset(page * limit).limit(limit).all()
    Meta.deserialize_meta_foreach(cars)

    return cars
  

  def add_car(self, creator_id, create_data: Car_Create):

    car = Car(**create_data.model_dump())
    Meta.add_meta(car, creator_id)

    self.db.add(car)
    self.db.commit()
    self.db.refresh(car)

    Meta.deserialize_meta(car)

    return car
  

  def update_car(self, updater_id, car_id, update_data: Car_Update):

    car = self.get_one(car_id)

    for field, value in update_data.model_dump(exclude_unset=True).items():
      setattr(car, field, value)

    Meta.update_meta(car, updater_id)

    self.db.commit()
    self.db.refresh(car)
    Meta.deserialize_meta(car)

    return car
  

  def delete_car(self, updater_id, car_id):

    car = self.get_one(car_id)

    car.is_active = False
    Meta.update_meta(car, updater_id)

    self.db.commit()

    return HttpResponse.ok_message("Автомобиль удален")

