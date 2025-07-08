#Author: Ian Surat-Mosher | Github: @iMosher
#Description: Schemas for Workout Tracker

from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

#Create Schemas
class SetCreate(BaseModel):
    reps: float
    weight: Optional[float] =None

class ExerciseCreate(BaseModel):
    name: str
    sets: List[SetCreate]

class TagCreate(BaseModel):
    name: str
    color: Optional[str] = None  # Optional hex or string

class WorkoutCreate(BaseModel):
    date: date
    exercises: List[ExerciseCreate]
    tags: Optional[List[TagCreate]] =[]

#Response Schemas
class SetResponse(BaseModel):
    id: int
    reps: float
    weight: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class ExerciseResponse(BaseModel):
    id: int
    name: str
    sets: List[SetResponse]

    model_config = ConfigDict(from_attributes=True)

class TagResponse(BaseModel):
    id: int
    name: str
    color: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
class WorkoutResponse(BaseModel):
    id: int
    date: date
    exercises: List[ExerciseResponse]
    tags: Optional[List[TagResponse]] = []

    model_config = ConfigDict(from_attributes=True)