from pydantic import BaseModel
from typing import List
from datetime import date

class Set(BaseModel):
    reps: int #number of reps
    weight: float #weight value (for now this is just a float with no unit; assume lbs)

class Exercise(BaseModel):
    name: str
    sets: List[Set]

class WorkoutCreate(BaseModel):
    date: date
    exercises: List[Exercise]

'''

Example JSON input for this schema:

{
  "date": "2025-07-01",
  "exercises": [
    {
      "name": "Deadlift",
      "sets": [
        { "reps": 5, "weight": 225.0 },
        { "reps": 5, "weight": 245.0 }
      ]
    }
  ]
}

'''