from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Set(BaseModel):
    reps: int #number of reps
    weight: float #weight value (for now this is just a float with no unit; assume lbs)

class Exercise(BaseModel):
    name: str
    sets: List[Set]

class SetCreate(BaseModel):
    reps: int
    weight: float

class ExerciseCreate(BaseModel):
    name: str
    sets: List[SetCreate]

class WorkoutCreate(BaseModel):
    date: date
    exercises: List[ExerciseCreate]

class SetResponse(BaseModel):
    reps: int
    weight: float

    class Config:
        orm_mode = True

class ExerciseResponse(BaseModel):
    name: str
    sets: List[SetResponse]

    class Config:
        orm_mode = True

class WorkoutResponse(BaseModel):
    id: int
    date: date
    exercises: List[ExerciseResponse]

    class Config:
        orm_mode = True


'''

Example JSON input for this schema:

{
  "date": "2025-07-02",
  "exercises": [
    {
      "name": "Squat",
      "sets": [
        { "reps": 5, "weight": 185 },
        { "reps": 5, "weight": 195 }
      ]
    },
    {
      "name": "Lunges",
      "sets": [
        { "reps": 8, "weight": 50 },
        { "reps": 8, "weight": 50 }
      ]
    }
  ]
}

'''