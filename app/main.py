from fastapi import FastAPI
from app.routers import users, workouts


app = FastAPI()

app.include_router(users.router, prefix="/users", tags = {"users"})
app.include_router(workouts.router, prefix="/workouts", tags=["workouts"])


@app.get("/")
def read_root():
    return {"message": "Workout Tracker API is running!"}