from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from models import Rental, RentalStatus
from utils import HttpResponse
from schemas import Meta, Rental_Create, Rental_TotalCost
from .car_usecases import Car_UseCases
from datetime import datetime, timezone, date


class Rental_UseCases:

  def __init__(self, db: Session):
    self.db = db
    self.car_usecases = Car_UseCases(db)


  def get_one(self, rental_id, user_id=None):

    query = self.db.query(Rental).filter(
        Rental.id == rental_id, Rental.is_active)

    if user_id:
      query = query.filter(Rental.user_id == user_id)

    rental = query.first()

    if not rental:
      raise HttpResponse.not_found("Аренда не найдена")

    Meta.deserialize_meta(rental)

    return rental


  def get_any(self, car_id=None, user_id=None, period_start: date = None, period_end: date = None, status=None, page=None, limit=None):

    query = self.db.query(Rental).filter(Rental.is_active == True)

    page = page if page else 0
    limit = limit if limit else 100

    if car_id:
      query = query.filter(Rental.car_id == car_id)
    if user_id:
      query = query.filter(Rental.user_id == user_id)
    if status:
      query = query.filter(Rental.status == status)

    if period_start and period_end:

      if period_start > period_end:
        raise HttpResponse.bad_request("Неверно указан период. Начальная дата должна быть меньше или равна конечной.")

      query = query.filter(or_(*[
        and_(Rental.start_date >= period_start, Rental.end_date <= period_end),
        and_(Rental.start_date < period_start, Rental.end_date > period_start, Rental.end_date <= period_end),
        and_(Rental.start_date >= period_start, Rental.start_date < period_end, Rental.end_date > period_end),
        and_(Rental.start_date < period_start, Rental.end_date > period_end),
      ]))

    rentals = query.order_by(desc(Rental.id)).offset(page * limit).limit(limit).all()
    Meta.deserialize_meta_foreach(rentals)

    return rentals


  def is_car_busy_in_period(self, car_id, period_start, period_end):

    if period_start > period_end:
      raise HttpResponse.bad_request("Неверно указан период. Начальная дата должна быть меньше или равна конечной.")

    rentals = self.get_any(car_id=car_id, period_start=period_start, period_end=period_end)

    for rental in rentals:
      if rental.status == RentalStatus.ACTIVE or rental.status == RentalStatus.PENDING:
        return True

    return False


  def get_rental_total_cost(self, create_data: Rental_Create):

    start_date = create_data.start_date
    end_date = create_data.end_date

    if datetime.now(timezone.utc).date() > start_date or start_date > end_date:
      raise HttpResponse.bad_request("Неверно указан период аренды. Начальная дата должна быть меньше или равна конечной дате и больше или равна текущей дате.")

    days = (end_date - start_date).days + 1

    if days > 60:
      raise HttpResponse.bad_request("Аренда на срок более 60 дней невозможна")

    car = self.car_usecases.get_one(create_data.car_id)
    price_per_day = car.price_per_day

    full_cost = price_per_day * days

    if days >= 30:
      discount = round(full_cost * 0.15, 2)  # 15% скидка
      message = "Скидка 15% за арнеду на срок 30+ дней"
    elif days >= 7:
      discount = round(full_cost * 0.1, 2)   # 10% скидка
      message = "Скидка 10% за арнеду на срок 7+ дней"
    else:
      discount = 0
      message = "Скидки не предусмотрены"

    total_cost = full_cost - discount
    
    return Rental_TotalCost(total_cost=total_cost, full_cost=full_cost, message=message)


  def create_rental(self, creator_id, user_id, create_data: Rental_Create):
    
    car_id, start_date, end_date = create_data.car_id, create_data.start_date, create_data.end_date
    total_cost = self.get_rental_total_cost(create_data).total_cost

    if self.is_car_busy_in_period(car_id, start_date, end_date):
      raise HttpResponse.bad_request("Автомобиль занят в этот период. Проверьте его распиание и выберите доступный период.")

    rental = Rental(**create_data.model_dump())
    rental.user_id = user_id
    rental.status = RentalStatus.PENDING
    rental.total_cost = total_cost
    Meta.add_meta(rental, creator_id)

    self.db.rollback()
    self.db.add(rental)
    self.db.commit()
    self.db.refresh(rental)
    Meta.deserialize_meta(rental)

    return rental


  def update_rental_status(self, updater_id, status, rental_id, user_id=None):
    
    rental = self.get_one(rental_id, user_id)

    pending_to_other = rental.status == RentalStatus.PENDING and status in [RentalStatus.ACTIVE, RentalStatus.CANCELLED]
    active_to_other = rental.status == RentalStatus.ACTIVE and status in [RentalStatus.COMPLETED]

    if not (pending_to_other or active_to_other):
      raise HttpResponse.bad_request("Недопустимое изменение статуса. Допустимые изменения: pending -> (active | cancelled), active -> completed")

    rental.status = status
    Meta.update_meta(rental, updater_id)

    self.db.commit()
    self.db.refresh(rental)
    Meta.deserialize_meta(rental)

    return rental


  def delete_rental(self, updater_id, rental_id, user_id=None):
    
    rental = self.get_one(rental_id, user_id)

    rental.is_active = False
    Meta.update_meta(rental, updater_id)

    self.db.commit()

    return HttpResponse.ok_message("Аренда удалена")


  