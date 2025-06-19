from datetime import datetime, timedelta, timezone
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
          full_name="Ivan Ivanov",
          role=UserRole.CLIENT,
      ),
  ]

  for item in users:
    Meta.add_meta(item, 1)

  session.add_all(users)

  # Cars
  cars = [
      Car(brand="Toyota", model="Camry", year=2022, type=CarType.SEDAN,
          price_per_day=3500.0, status=CarStatus.AVAILABLE),
      Car(brand="Kia", model="Rio", year=2021, type=CarType.SEDAN,
          price_per_day=2500.0, status=CarStatus.AVAILABLE),
      Car(brand="Hyundai", model="Creta", year=2023, type=CarType.SUV,
          price_per_day=4000.0, status=CarStatus.RENTED),
      Car(brand="Volkswagen", model="Polo", year=2020, type=CarType.HATCHBACK,
          price_per_day=2800.0, status=CarStatus.AVAILABLE),
      Car(brand="Skoda", model="Octavia", year=2022, type=CarType.SEDAN,
          price_per_day=3800.0, status=CarStatus.MAINTENANCE),
      Car(brand="BMW", model="X5", year=2021, type=CarType.SUV,
          price_per_day=8500.0, status=CarStatus.AVAILABLE),
      Car(brand="Audi", model="A4", year=2022, type=CarType.SEDAN,
          price_per_day=6500.0, status=CarStatus.AVAILABLE),
      Car(brand="Mercedes-Benz", model="C-Class", year=2023,
          type=CarType.COUPE, price_per_day=7500.0, status=CarStatus.RENTED),
      Car(brand="Lada", model="Granta", year=2022, type=CarType.SEDAN,
          price_per_day=1800.0, status=CarStatus.AVAILABLE),
      Car(brand="Renault", model="Duster", year=2021, type=CarType.SUV,
          price_per_day=3500.0, status=CarStatus.AVAILABLE),
      Car(brand="Ford", model="Focus", year=2020, type=CarType.HATCHBACK,
          price_per_day=3000.0, status=CarStatus.MAINTENANCE),
      Car(brand="Mazda", model="CX-5", year=2022, type=CarType.SUV,
          price_per_day=4500.0, status=CarStatus.AVAILABLE),
      Car(brand="Nissan", model="Qashqai", year=2021, type=CarType.SUV,
          price_per_day=4200.0, status=CarStatus.AVAILABLE),
      Car(brand="Toyota", model="RAV4", year=2023, type=CarType.SUV,
          price_per_day=5500.0, status=CarStatus.RENTED),
      Car(brand="Chevrolet", model="Camaro", year=2022, type=CarType.COUPE,
          price_per_day=9000.0, status=CarStatus.AVAILABLE),
      Car(brand="Volkswagen", model="Tiguan", year=2021, type=CarType.SUV,
          price_per_day=4800.0, status=CarStatus.AVAILABLE),
      Car(brand="Hyundai", model="Solaris", year=2020, type=CarType.SEDAN,
          price_per_day=2200.0, status=CarStatus.AVAILABLE),
      Car(brand="Kia", model="Sportage", year=2022, type=CarType.SUV,
          price_per_day=4700.0, status=CarStatus.AVAILABLE),
      Car(brand="BMW", model="3 Series", year=2023, type=CarType.SEDAN,
          price_per_day=7000.0, status=CarStatus.MAINTENANCE),
      Car(brand="Audi", model="Q5", year=2021, type=CarType.SUV,
          price_per_day=6800.0, status=CarStatus.AVAILABLE)
  ]

  for item in cars:
    Meta.add_meta(item, 2)

  session.add_all(cars)

  # Rentals
  now = datetime.now(timezone.utc).date()

  rentals = [
      Rental(
          user_id=3,
          car_id=1,
          start_date=now - timedelta(days=5),
          end_date=now + timedelta(days=2),
          total_cost=7 * 3500.0,
          status=RentalStatus.ACTIVE
      ),
      Rental(
          user_id=4,
          car_id=3,
          start_date=now - timedelta(days=10),
          end_date=now - timedelta(days=3),
          total_cost=7 * 4000.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=5,
          start_date=now + timedelta(days=2),
          end_date=now + timedelta(days=7),
          total_cost=5 * 3800.0,
          status=RentalStatus.PENDING
      ),
      Rental(
          user_id=4,
          car_id=7,
          start_date=now - timedelta(days=15),
          end_date=now - timedelta(days=8),
          total_cost=7 * 6500.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=8,
          start_date=now - timedelta(days=3),
          end_date=now + timedelta(days=4),
          total_cost=7 * 7500.0,
          status=RentalStatus.ACTIVE
      ),
      Rental(
          user_id=4,
          car_id=10,
          start_date=now - timedelta(days=20),
          end_date=now - timedelta(days=13),
          total_cost=7 * 3500.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=11,
          start_date=now - timedelta(days=1),
          end_date=now + timedelta(days=6),
          total_cost=7 * 3000.0,
          status=RentalStatus.ACTIVE
      ),
      Rental(
          user_id=4,
          car_id=14,
          start_date=now - timedelta(days=7),
          end_date=now - timedelta(days=1),
          total_cost=6 * 5500.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=15,
          start_date=now + timedelta(days=5),
          end_date=now + timedelta(days=12),
          total_cost=7 * 9000.0,
          status=RentalStatus.PENDING
      ),
      Rental(
          user_id=4,
          car_id=16,
          start_date=now - timedelta(days=14),
          end_date=now - timedelta(days=7),
          total_cost=7 * 4800.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=18,
          start_date=now - timedelta(days=2),
          end_date=now + timedelta(days=5),
          total_cost=7 * 4700.0,
          status=RentalStatus.ACTIVE
      ),
      Rental(
          user_id=4,
          car_id=19,
          start_date=now - timedelta(days=30),
          end_date=now - timedelta(days=23),
          total_cost=7 * 7000.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=20,
          start_date=now - timedelta(days=4),
          end_date=now + timedelta(days=3),
          total_cost=7 * 6800.0,
          status=RentalStatus.ACTIVE
      ),
      Rental(
          user_id=4,
          car_id=2,
          start_date=now - timedelta(days=8),
          end_date=now - timedelta(days=1),
          total_cost=7 * 2500.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=6,
          start_date=now + timedelta(days=3),
          end_date=now + timedelta(days=10),
          total_cost=7 * 8500.0,
          status=RentalStatus.PENDING
      ),
      Rental(
          user_id=4,
          car_id=9,
          start_date=now - timedelta(days=12),
          end_date=now - timedelta(days=5),
          total_cost=7 * 1800.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=12,
          start_date=now - timedelta(days=6),
          end_date=now + timedelta(days=1),
          total_cost=7 * 4500.0,
          status=RentalStatus.ACTIVE
      ),
      Rental(
          user_id=4,
          car_id=13,
          start_date=now - timedelta(days=9),
          end_date=now - timedelta(days=2),
          total_cost=7 * 4200.0,
          status=RentalStatus.COMPLETED
      ),
      Rental(
          user_id=3,
          car_id=4,
          start_date=now + timedelta(days=1),
          end_date=now + timedelta(days=8),
          total_cost=7 * 2800.0,
          status=RentalStatus.PENDING
      ),
      Rental(
          user_id=4,
          car_id=17,
          start_date=now - timedelta(days=25),
          end_date=now - timedelta(days=18),
          total_cost=7 * 2200.0,
          status=RentalStatus.COMPLETED
      )
  ]

  for item in rentals:
    Meta.add_meta(item, item.user_id)

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
