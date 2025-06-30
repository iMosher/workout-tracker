from app.database import engine, Base
from app.models import Workout, Exercise

Base.metadata.create_all(bind=engine)

print("Workout and Exercise tables created!")