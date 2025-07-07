#Author: Ian Surat-Mosher | Github: @iMosher
#Description: API endpoints for users
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def say_hello():
    return {"message": "Hello from the users router!"}