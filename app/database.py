from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLite URL for SQAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./workout_tracker.db"

#connect_args needed for SQLite to allow multithreading
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#SessionLocal class instance will be the actual DB session
SessionLocal = sessionmaker(autocommit=False, autoflush =False, bind=engine)

#Base class for models
Base = declarative_base()
