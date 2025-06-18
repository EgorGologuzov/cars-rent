from datetime import datetime, timedelta
from database import Base, engine, get_db
from models import User, UserRole, Car, CarType, CarStatus, Rental, RentalStatus, Review
from auth import get_password_hash
from schemas import Meta


with get_db().__next__() as session:

  # Создание и удаление таблиц
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)

  # Users
  users = [
      User(
          email="admin@example.com",
          hashed_password=get_password_hash("12345678"),
          full_name="Admin Adminov",
          role=UserRole.ADMIN,
      ),
      User(
          email="manager@example.com",
          hashed_password=get_password_hash("12345678"),
          full_name="Manager Managerov",
          role=UserRole.MANAGER,
      ),
      User(
          email="client@example.com",
          hashed_password=get_password_hash("12345678"),
          full_name="Client Clientov",
          role=UserRole.CLIENT,
      ),
      User(
          email="user@example.com",
          hashed_password=get_password_hash("12345678"),
          full_name="Petr Petrov",
          role=UserRole.CLIENT,
      )
  ]

  for item in users:
    Meta.add_meta(item, 1)

  session.add_all(users)

  # Cars
  cars = [
      Car(
          brand="Toyota",
          model="Camry",
          year=2022,
          type=CarType.SEDAN,
          price_per_day=2500.0,
          status=CarStatus.AVAILABLE,
      ),
      Car(
          brand="BMW",
          model="X5",
          year=2021,
          type=CarType.SUV,
          price_per_day=4000.0,
          status=CarStatus.RENTED,
      ),
      Car(
          brand="Ford",
          model="Mustang",
          year=2023,
          type=CarType.COUPE,
          price_per_day=3750.0,
          status=CarStatus.AVAILABLE,
      ),
      Car(
          brand="Volkswagen",
          model="Golf",
          year=2020,
          type=CarType.HATCHBACK,
          price_per_day=2000.0,
          status=CarStatus.MAINTENANCE,
      )
  ]

  for item in cars:
    Meta.add_meta(item, 1)

  session.add_all(cars)

  # Rentals
  rentals = [
      Rental(
          user_id=3,
          car_id=2,
          start_date=datetime.now() - timedelta(days=5),
          end_date=datetime.now() + timedelta(days=5),
          total_cost=20_000.0,
          status=RentalStatus.ACTIVE,
      ),
      Rental(
          user_id=4,
          car_id=1,
          start_date=datetime.now() - timedelta(days=10),
          end_date=datetime.now() - timedelta(days=3),
          total_cost=17_500.0,
          status=RentalStatus.COMPLETED,
      )
  ]

  for item in rentals:
    Meta.add_meta(item, 1)

  session.add_all(rentals)

  # Reviews
  reviews = [
      Review(
          car_id=2,
          user_id=3,
          rating=4,
          comment="Great car but a bit expensive",
      ),
      Review(
          car_id=1,
          user_id=4,
          rating=5,
          comment="Perfect car for family trips",
      )
  ]

  for item in reviews:
    Meta.add_meta(item, 1)

  session.add_all(reviews)

  session.commit()

  print("Данные успешно добавлены в базу данных!")

