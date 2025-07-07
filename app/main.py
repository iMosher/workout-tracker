#Author: Ian Surat-Mosher | Github: @iMosher

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, workouts


app = FastAPI()

#CORS Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Routers
app.include_router(users.router, prefix="/users", tags = {"users"})
app.include_router(workouts.router, prefix="/workouts", tags=["workouts"])


@app.get("/")
def read_root():
    return {"message": "Workout Tracker API is running!"}