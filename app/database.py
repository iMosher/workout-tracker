from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#SQLite URL for SQAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./workout_tracker.db"

#Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#connect_args needed for SQLite to allow multithreading
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#SessionLocal class instance will be the actual DB session
SessionLocal = sessionmaker(autocommit=False, autoflush =False, bind=engine)

#Base class for models
Base = declarative_base()
