from app.database import engine, Base
from app.models import Workout, Exercise, Set, Tag, workout_tag_association

Base.metadata.create_all(bind=engine)

print("Workout, Set, and Exercise and Tag tables created!")