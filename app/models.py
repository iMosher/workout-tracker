#Author: Ian Surat-Mosher | Github: @iMosher
#Description: Model classes for Workout Tracker

from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base


workout_tag_association = Table(
    "workout_tag_association",
    Base.metadata,
    Column("workout_id", Integer, ForeignKey("workouts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)

    exercises = relationship("Exercise", back_populates="workout", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=workout_tag_association, back_populates="workouts")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id")) #replace eventually

    workout = relationship("Workout",back_populates="exercises")
    sets = relationship("Set", back_populates="exercise", cascade="all, delete-orphan")

class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    reps =Column(Float, nullable=False) # this is an integer for the time being, add partial reps later
    weight = Column(Float, nullable=True) #Weight is optional allowing for bodyweight exercises

    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise", back_populates="sets")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    color =Column(String, nullable=True)

    workouts = relationship("Workout", secondary=workout_tag_association, back_populates="tags")