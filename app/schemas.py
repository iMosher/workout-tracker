from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

#Create Schemas
class SetCreate(BaseModel):
    reps: int
    weight: float

class ExerciseCreate(BaseModel):
    name: str
    sets: List[SetCreate]

class WorkoutCreate(BaseModel):
    date: date
    exercises: List[ExerciseCreate]


#Response Schemas
class SetResponse(BaseModel):
    id: int
    reps: int
    weight: float

    model_config = ConfigDict(from_attributes=True)

class ExerciseResponse(BaseModel):
    id: int
    name: str
    sets: List[SetResponse]

    model_config = ConfigDict(from_attributes=True)

class WorkoutResponse(BaseModel):
    id: int
    date: date
    exercises: List[ExerciseResponse]

    model_config = ConfigDict(from_attributes=True)
