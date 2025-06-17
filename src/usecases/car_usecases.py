from sqlalchemy.orm import Session
from models import Car
from utils import HttpResponse
from schemas import Meta


class Car_UseCases:

  def __init__(self, db: Session):
    self.db = db


  def get_any(self, type, status, min_year, page, limit):
    query = self.db.query(Car)

    page = page if page else 0
    limit = limit if limit else 100

    if type:
      query = query.filter(Car.type == type)
    if status:
      query = query.filter(Car.status == status)
    if min_year:
      query = query.filter(Car.year >= min_year)

    cars = query.offset(page * limit).limit(limit).all()
    Meta.deserialize_meta_foreach(cars)

    return cars


  def get_one(self, car_id):
    car = self.db.query(Car).filter(Car.id == car_id).first()

    if not car:
      raise HttpResponse.not_found("Автомобиль не найден")
    
    Meta.deserialize_meta(car)
  
    return car
  

  def add_car(self, **car_data):
    car = Car(**car_data)
    Meta.add_meta(car, 1)

    self.db.add(car)
    self.db.commit()
    self.db.refresh(car)

    Meta.deserialize_meta(car)

    return car
  

  def update_car(self, car_id, **car_data):
    car = self.db.query(Car).filter(Car.id == car_id).first()

    if not car:
      raise HttpResponse.not_found("Автомобиль не найден")

    for field, value in car_data.items():
      setattr(car, field, value)

    Meta.update_meta(car, 1)

    self.db.commit()
    self.db.refresh(car)

    Meta.deserialize_meta(car)

    return car
  

  def delete_car(self, car_id):
    car = self.db.query(Car).filter(Car.id == car_id).first()
  
    if not car:
      raise HttpResponse.not_found("Автомобиль не найден")

    self.db.delete(car)
    self.db.commit()

    return HttpResponse.ok_message("Автомобиль удален")

