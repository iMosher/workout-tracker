#Author: Ian Surat-Mosher | Github: @iMosher
#Description: API Endpoints for Workout Data

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from app.database import get_db
from app.models import Workout, Exercise, Set
from app.schemas import WorkoutCreate, WorkoutResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=WorkoutResponse)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(date=workout.date)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    for exercise in workout.exercises:
        db_exercise = Exercise(name=exercise.name, workout_id=db_workout.id)
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)

        for set_data in exercise.sets:
            db_set = Set(reps=set_data.reps, weight=set_data.weight, exercise_id=db_exercise.id)
            db.add(db_set)
    
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.get("/", response_model=List[WorkoutResponse])
def get_all_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).options(
        selectinload(Workout.exercises).selectinload(Exercise.sets)
    ).all()

@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout_by_id(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).options(
        selectinload(Workout.exercises).selectinload(Exercise.sets)
    ).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(workout_id: int, updated_workout: WorkoutCreate, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Delete existing sets and exercises
    for exercise in workout.exercises:
        for set_ in exercise.sets:
            db.delete(set_)
        db.delete(exercise)
    db.commit()

    workout.date = updated_workout.date
    db.commit()

    for exercise_data in updated_workout.exercises:
        db_exercise = Exercise(name=exercise_data.name, workout_id=workout.id)
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        
        for set_data in exercise_data.sets:
            db_set = Set(reps=set_data.reps, weight=set_data.weight, exercise_id=db_exercise.id)
            db.add(db_set)
    
    db.commit()
    db.refresh(workout)
    return workout

@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.delete(workout)
    db.commit()
