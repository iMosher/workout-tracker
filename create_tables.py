from app.database import engine, Base
from app.models import Workout, Exercise, Set

Base.metadata.create_all(bind=engine)

print("Workout, Set, and Exercise tables created!")