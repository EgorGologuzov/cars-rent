from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLIGHT_DATABASE_URL = "sqlite:///./database.sqlite"

Base = declarative_base()

engine = create_engine(
  SQLIGHT_DATABASE_URL,
  connect_args={"check_same_thread": False}
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
  db = Session()
  try:
    yield db
  finally:
      db.close()

