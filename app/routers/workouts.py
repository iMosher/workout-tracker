from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from app.database import SessionLocal
from app.models import Workout, Exercise
from app.schemas import WorkoutCreate

router = APIRouter()

#Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#POST a new Workout
@router.post("/", tags=["workouts"])
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    #Create Workout record
    db_workout = Workout(date=workout.date)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    #Create Exercise records
    for exercise in workout.exercises:
        db_exercise = Exercise(name=exercise.name, workout_id=db_workout.id)
        db.add(db_exercise)
        db.commit()
    
    return{
        "id": db_workout.id, 
        "date": str(db_workout.date), 
        "exercises": [e.name for e in workout.exercises]
    }

#GET all Workouts
@router.get("/", tags=["workouts"])
def get_all_workouts(db: Session = Depends(get_db)):
    workouts = db.query(Workout).options(selectinload(Workout.exercises)).all()
    return [
        {
            "id": workout.id,
            "date": str(workout.date),
            "exercises": [exercise.name for exercise in workout.exercises]
        }
        for workout in workouts
    ]


#GET workout by id
@router.get("/{workout_id}", tags=["workouts"])
def get_workout_by_id(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).options(selectinload(Workout.exercises)).filter(Workout.id == workout_id).first()
    if not workout:
        return {"error": "Workout not found"}
    
    return {
        "id": workout.id,
        "date": str(workout.date),
        "exercises": [exercise.name for exercise in workout.exercises]
    }