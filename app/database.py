from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings


SQLALCHEMY_DATABASE_URL = (
    "postgresql://{username}:{password}@{hostname}:{port}/{db_name}".format(
        username=settings.database_username,
        password=settings.database_password,
        hostname=settings.database_hostname,
        port=settings.database_port,
        db_name=settings.database_name,
    )
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
