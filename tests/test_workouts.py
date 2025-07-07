#Author: Ian Surat-Mosher | Github: @iMosher
#Description: Testing for API endpoints

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Add project root to sys.path

# Use a seperate test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_workout_tracker.db"

# Test Engine and session setup
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clear testing db and override depenecies
@pytest.fixture(scope="module")
def test_db():

    # Drop & recreate tabes
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    #Override dependencies
    def ovveride_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = ovveride_get_db
    client = TestClient(app)

    yield client #Tests will use this client

    engine.dispose()
    os.remove("test_workout_tracker.db")

#Test POST Workout endpoint
def test_create_workout(test_db):

    #POST request
    response = test_db.post(
        "/workouts/",
        json={
            "date": "2025-07-03",
            "exercises": [
                {
                    "name": "Bench Press",
                    "sets": [
                        {"reps": 5.0, "weight": 135.0},
                        {"reps": 5.0, "weight": 145.0}
                    ]
                }
            ]
        },
    )
    
    #Tests
    assert response.status_code == 200
    data = response.json()
    assert data["date"] == "2025-07-03"
    assert len(data["exercises"]) == 1
    assert data["exercises"][0]["name"] == "Bench Press"

#Test GET all workouts:
def test_get_all_workouts(test_db):
    # Create a workout
    test_db.post(
        "/workouts/",
        json={
            "date": "2025-07-04",
            "exercises": [
                {
                    "name": "Deadlift",
                    "sets": [{"reps": 3.0, "weight": 315.0}]
                }
            ]
        }
    )
    #Fetch all workouts
    response = test_db.get("/workouts/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert any(w["date"] == "2025-07-04" for w in data)

# Test GET workout by ID
def test_get_workout_by_id(test_db):
    #Create a new workout
    post_response = test_db.post(
        "/workouts/",
        json={
            "date": "2025-07-05",
            "exercises": [
                {
                    "name": "Overhead Press",
                    "sets": [{"reps": 5.0, "weight": 95.0}]
                }
            ]
        }
    )

    assert post_response.status_code == 200
    workout_id = post_response.json()["id"]

    #now retrieve workout by ID
    get_response = test_db.get(f"/workouts/{workout_id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["id"] == workout_id
    assert data["date"] == "2025-07-05"
    assert data["exercises"][0]["name"] == "Overhead Press"
    assert data["exercises"][0]["sets"][0]["reps"] == 5.0
    assert data["exercises"][0]["sets"][0]["weight"] == 95.0

#Test Updating a workout via POST and PUT endpoints
def test_update_workout(test_db):
    # Create initial workout
    post_response = test_db.post(
        "/workouts/",
        json={
            "date": "2025-07-06",
            "exercises": [
                {
                    "name": "Bent Over Row",
                    "sets": [{"reps": 8.0, "weight": 115.0}]
                }
            ]
        }
    )
    assert post_response.status_code == 200
    workout_id = post_response.json()["id"]

    # Update via PUT endpoint
    put_response = test_db.put(

        f"/workouts/{workout_id}",
        json={
            "date": "2025-07-07",  # updated date
            "exercises": [
                {
                    "name": "Incline Bench",
                    "sets": [{"reps": 10.0, "weight": 95.0}]
                }
            ]
        }
    )

    assert put_response.status_code == 200
    updated_data = put_response.json()

    assert updated_data["date"] == "2025-07-07"
    assert updated_data["exercises"][0]["name"] == "Incline Bench"
    assert updated_data["exercises"][0]["sets"][0]["reps"] == 10.0
    assert updated_data["exercises"][0]["sets"][0]["weight"] == 95.0

#Test DELETE endpoint
def test_delete_workout(test_db):
    #Create workout
    post_response = test_db.post(
        "/workouts/",
        json={
            "date": "2025-07-08",
            "exercises": [
                {
                    "name": "Overhead Press",
                    "sets": [{"reps": 6.0, "weight": 85.0}]
                }
            ]
        }
    )
    assert post_response.status_code == 200
    workout_id = post_response.json()["id"]

    #Delete the workout
    delete_response = test_db.delete(f"/workouts/{workout_id}")
    assert delete_response.status_code == 204

    #Attempt to fetch deleted workout
    get_response = test_db.get(f"/workouts/{workout_id}")
    assert get_response.status_code == 404